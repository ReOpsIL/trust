use crossterm::event::{KeyEvent, KeyCode, KeyModifiers};
use crate::editor::buffer::TextBuffer;
use crate::editor::keyboard::{Keyboard, ModifierState};
use crate::editor::printer::Printer;

pub enum WritingMode {
    Insert,
    Overwrite,
}

pub struct App {
    keyboard: Keyboard,
    printer: Printer,
    buffer: TextBuffer,
    writing_mode: WritingMode,
    exit_count: i8,
    shift_mode: bool,
    ctrl_mode: bool,
    alt_mode: bool,
    command_mode: bool, // For Mac
    windows_mode: bool, // For Windows
}

impl App {
    pub fn new() -> Self {
        Self {
            keyboard: Keyboard::new(),
            printer: Printer::new(),
            buffer: TextBuffer::new(),
            writing_mode: WritingMode::Insert,
            exit_count: 0,
            shift_mode: false,
            ctrl_mode: false,
            alt_mode: false,
            command_mode: false,
            windows_mode: false,
        }
    }

    // Ensure the cursor is visible in the viewport
    fn ensure_cursor_visible(&mut self) {
        let cursor_line = self.buffer.get_cursor_line();
        let viewport_start = self.printer.get_viewport_start();
        let viewport_height = self.printer.get_viewport_height();

        // If cursor is above viewport, adjust viewport to show cursor
        if cursor_line < viewport_start {
            self.printer.set_viewport_start(cursor_line);
        }
        // If cursor is below viewport, adjust viewport to show cursor
        else if cursor_line >= viewport_start + viewport_height {
            self.printer.set_viewport_start(cursor_line - viewport_height + 1);
        }
    }

    pub fn run(&mut self) {
        self.printer.clear_screen();
        self.printer.print_buffer(
            self.buffer.get_buffer_content(),
            self.buffer.get_cursor_line(),
            self.buffer.get_cursor_col()
        );

        loop {
            match (&mut self.keyboard).get_key() {
                Ok(key_event) => {
                    if key_event.code == KeyCode::Null {
                        continue;
                    }
                    let modifiers = self.keyboard.get_modifier_state();
                    self.shift_mode = modifiers.shift;
                    self.ctrl_mode = modifiers.ctrl;
                    self.alt_mode = modifiers.alt;
                    self.command_mode = modifiers.meta; // Command key on macOS
                    self.windows_mode = modifiers.meta; // Windows key on Windows

                    if key_event.code != KeyCode::Esc {
                        self.exit_count = 0;   
                    }
                    match key_event.code {
                        KeyCode::Left => {
                            if self.shift_mode && !self.ctrl_mode {
                                self.buffer.select_char_left();
                            }
                            else if self.shift_mode && self.ctrl_mode {
                                self.buffer.select_word_left();
                            }
                            else {
                                self.buffer.move_cursor_left();
                            }
                        },
                        KeyCode::Right => {
                            if self.shift_mode && !self.ctrl_mode {
                                self.buffer.select_char_right();
                            }
                            else if self.shift_mode && self.ctrl_mode {
                                self.buffer.select_word_right();
                            }
                            else {
                                self.buffer.move_cursor_right();
                            }
                        },
                        KeyCode::Up => {
                            if self.shift_mode {
                                self.buffer.select_line_up()
                            }
                            else {
                                self.buffer.move_cursor_up();
                            }

                            // If cursor moves up, we might need to scroll up
                            if self.buffer.get_cursor_line() < self.printer.get_viewport_start() {
                                self.printer.scroll_up();
                            }
                        },
                        KeyCode::Down => {
                            if self.shift_mode {
                                self.buffer.select_line_down()
                            }
                            else {
                                self.buffer.move_cursor_down();
                            }

                            // If cursor moves down, we might need to scroll down
                            let viewport_end = self.printer.get_viewport_start() + self.printer.get_viewport_height() - 1;
                            if self.buffer.get_cursor_line() > viewport_end {
                                self.printer.scroll_down(self.buffer.get_line_count());
                            }
                        },
                        KeyCode::Enter => {
                            self.buffer.insert_newline();
                            // After inserting a newline, we might need to scroll down
                            let viewport_end = self.printer.get_viewport_start() + self.printer.get_viewport_height() - 1;
                            if self.buffer.get_cursor_line() > viewport_end {
                                self.printer.scroll_down(self.buffer.get_line_count());
                            }
                        },
                        KeyCode::Esc => {
                            self.exit_count+=1;
                            if self.exit_count > 5 {
                                // Exit the application
                                return;    
                            }

                        },
                        KeyCode::Backspace => {
                            self.buffer.delete_char_before_cursor();
                        },
                        KeyCode::Home => {
                            self.buffer.move_cursor_to_beginning_of_line();
                        },
                        KeyCode::End => {
                            self.buffer.move_cursor_to_end_of_line();
                        },
                        KeyCode::Tab => {
                            self.buffer.insert_char('\t');
                        },
                        KeyCode::BackTab => {},
                        KeyCode::Delete => {
                            self.buffer.delete_char_at_cursor();
                        },
                        KeyCode::Insert => {
                            match self.writing_mode {
                                WritingMode::Insert => {
                                    self.writing_mode = WritingMode::Overwrite;
                                },
                                WritingMode::Overwrite => {
                                    self.writing_mode = WritingMode::Insert;   
                                }
                            }
                        },
                        KeyCode::PageUp => {
                            // Move cursor up by viewport height
                            for _ in 0..self.printer.get_viewport_height() {
                                self.buffer.move_cursor_up();
                            }
                            // Adjust viewport
                            let new_viewport_start = self.printer.get_viewport_start().saturating_sub(self.printer.get_viewport_height());
                            self.printer.set_viewport_start(new_viewport_start);
                        },
                        KeyCode::PageDown => {
                            // Move cursor down by viewport height
                            for _ in 0..self.printer.get_viewport_height() {
                                self.buffer.move_cursor_down();
                            }
                            // Adjust viewport
                            let new_viewport_start = self.printer.get_viewport_start() + self.printer.get_viewport_height();
                            let max_start = self.buffer.get_line_count().saturating_sub(self.printer.get_viewport_height());
                            self.printer.set_viewport_start(new_viewport_start.min(max_start));
                        },
                        KeyCode::Char(c) => {
                            if self.ctrl_mode {
                                match c {
                                    'c' => {
                                        self.buffer.copy_selected_text();
                                    },
                                    'v' => {
                                        self.buffer.paste();
                                    },
                                    'x' => {
                                        self.buffer.cut_selected_text();
                                    },
                                    'a' => {
                                        self.buffer.select_all();
                                    },
                                    'z' => {
                                        if self.shift_mode {
                                            self.buffer.redo();
                                        }
                                        else {
                                            self.buffer.undo();
                                        }
                                    },
                                    _ => {
                                        self.buffer.insert_char(c);
                                    }
                                }
                            } else {
                                self.buffer.insert_char(c);
                            }
                        },
                        _ => {
                            //print!("{:?}", key_event)
                        }
                    }

                    // Ensure cursor is visible after any operation
                    self.ensure_cursor_visible();

                    // Print the visible portion of the buffer
                    self.printer.print_buffer(
                        self.buffer.get_buffer_content(),
                        self.buffer.get_cursor_line(),
                        self.buffer.get_cursor_col()
                    );

                   //  // Print the current state of modifier keys
                   // println!("Modifier keys: Shift={}, Ctrl={}, Alt={}, Command={}, Windows={}",
                   //      self.shift_mode, self.ctrl_mode, self.alt_mode, self.command_mode, self.windows_mode);
                },
                Err(e) => println!("Error getting key: {e:?}"),
            }
        }
    }
}
