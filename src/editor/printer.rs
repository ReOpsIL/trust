use std::io::Write;
use console::{Key, Term};

pub struct Printer {
    last_key: Key,
    term: Term
}

impl Printer {

    pub fn new() -> Self {
        Self {
            last_key:  Key::Unknown,
            term: Term::stdout()
        }
    }
    
    pub fn clear_screen(&mut self) {
        self.term.clear_screen();
    }
    pub fn print_buffer(&mut self, text: String) {
        self.term.clear_screen();
        self.term.write_line(text.as_str());
    }
    pub fn print(&mut self, key : Key) {
        self.last_key = key;
        // print!("{:?}", self.last_key);
        match self.last_key {
            Key::Char(c) => {
                let _ = self.term.write(format!("{}", c).as_bytes());
            },
            Key::Enter => {
                self.term.write_line("");                
            }
            _ => {
               
            }
        }
        // self.term.write(format!("{}", self.last_key).as_bytes());
        // self.term.flush();
    }
}

