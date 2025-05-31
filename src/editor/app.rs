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

    pub fn run(&mut self) {
        self.printer.clear_screen();
        
        loop {
            match self.keyboard.get_key() {
                Ok(key) => {
                    match key {
                        Key::ArrowLeft => {},
                        Key::ArrowRight => {},
                        Key::ArrowUp => {},
                        Key::ArrowDown => {},
                        Key::Enter => {
                            self.buffer.insert_newline()
                        },
                        Key::Escape => {
                            
                        },
                        Key::Backspace => {
                            self.buffer.delete_char_before_cursor()
                        },
                        Key::Home => {
                            self.buffer.move_cursor_to_beginning_of_line()
                        },
                        Key::End => {
                            self.buffer.move_cursor_to_end_of_line()
                        },
                        Key::Tab => {
                            self.buffer.insert_char('\t')
                        },
                        Key::BackTab => {},
                        Key::Alt => {},
                        Key::Del => {
                            self.buffer.delete_char_at_cursor()
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
                            self.buffer.move_cursor_up();
                        },
                        Key::PageDown => {
                            self.buffer.move_cursor_down();
                        },
                        Key::Char(char) => {
                            self.buffer.insert_char(char);
                        },
                        Key::CtrlC => {
                            self.buffer.copy_selected_text();
                        },
                        _ => {
                            println!("Unknown key: {:?}", key);
                        }
                    }
                    self.printer.print_buffer(self.buffer.get_buffer_content())
                },
                Err(e) => println!("Error getting key: {e:?}"),
            }
        }
    }
}