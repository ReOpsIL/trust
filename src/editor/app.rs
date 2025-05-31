use console::Key;
use crate::editor::buffer::TextBuffer;
use crate::editor::keyboard::Keyboard;
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
}

impl App {
    pub fn new() -> Self {
        Self {
            keyboard: Keyboard::new(),
            printer: Printer::new(),
            buffer: TextBuffer::new(),
            writing_mode: WritingMode::Insert,       
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
            match self.keyboard.get_key() {
                Ok(key) => {
                    match key {
                        Key::ArrowLeft => {
                            self.buffer.move_cursor_left();
                        },
                        Key::ArrowRight => {
                            self.buffer.move_cursor_right();
                        },
                        Key::ArrowUp => {
                            self.buffer.move_cursor_up();
                            // If cursor moves up, we might need to scroll up
                            if self.buffer.get_cursor_line() < self.printer.get_viewport_start() {
                                self.printer.scroll_up();
                            }
                        },
                        Key::ArrowDown => {
                            self.buffer.move_cursor_down();
                            // If cursor moves down, we might need to scroll down
                            let viewport_end = self.printer.get_viewport_start() + self.printer.get_viewport_height() - 1;
                            if self.buffer.get_cursor_line() > viewport_end {
                                self.printer.scroll_down(self.buffer.get_line_count());
                            }
                        },
                        Key::Enter => {
                            self.buffer.insert_newline();
                            // After inserting a newline, we might need to scroll down
                            let viewport_end = self.printer.get_viewport_start() + self.printer.get_viewport_height() - 1;
                            if self.buffer.get_cursor_line() > viewport_end {
                                self.printer.scroll_down(self.buffer.get_line_count());
                            }
                        },
                        Key::Escape => {
                            // Exit the application
                            return;
                        },
                        Key::Backspace => {
                            self.buffer.delete_char_before_cursor();
                        },
                        Key::Home => {
                            self.buffer.move_cursor_to_beginning_of_line();
                        },
                        Key::End => {
                            self.buffer.move_cursor_to_end_of_line();
                        },
                        Key::Tab => {
                            self.buffer.insert_char('\t');
                        },
                        Key::BackTab => {},
                        Key::Alt => {},
                        Key::Del => {
                            self.buffer.delete_char_at_cursor();
                        },
                        Key::Shift => {},
                        Key::Insert => {
                            match self.writing_mode {
                                WritingMode::Insert => {
                                    self.writing_mode = WritingMode::Overwrite;
                                },
                                WritingMode::Overwrite => {
                                    self.writing_mode = WritingMode::Insert;   
                                }
                            }
                        },
                        Key::PageUp => {
                            // Move cursor up by viewport height
                            for _ in 0..self.printer.get_viewport_height() {
                                self.buffer.move_cursor_up();
                            }
                            // Adjust viewport
                            let new_viewport_start = self.printer.get_viewport_start().saturating_sub(self.printer.get_viewport_height());
                            self.printer.set_viewport_start(new_viewport_start);
                        },
                        Key::PageDown => {
                            // Move cursor down by viewport height
                            for _ in 0..self.printer.get_viewport_height() {
                                self.buffer.move_cursor_down();
                            }
                            // Adjust viewport
                            let new_viewport_start = self.printer.get_viewport_start() + self.printer.get_viewport_height();
                            let max_start = self.buffer.get_line_count().saturating_sub(self.printer.get_viewport_height());
                            self.printer.set_viewport_start(new_viewport_start.min(max_start));
                        },
                        Key::Char(char) => {
                            self.buffer.insert_char(char);
                        },
                        Key::CtrlC => {
                            self.buffer.copy_selected_text();
                        },
                        _ => {
                            // Ignore unknown keys
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
                },
                Err(e) => println!("Error getting key: {e:?}"),
            }
        }
    }
}
