use std::io;
use crossterm::event::{self, Event, KeyEvent, KeyCode, KeyModifiers};
use crossterm::terminal;

pub(crate) struct Keyboard {
    last_key_pressed: KeyCode,
    last_modifiers: KeyModifiers,
    last_char: Option<char>
}

// Define a struct to hold modifier key states
pub struct ModifierState {
    pub shift: bool,
    pub ctrl: bool,
    pub alt: bool,
    pub meta: bool, // Command key on macOS, Windows key on Windows
}

impl Keyboard {
    pub fn new() -> Self {
        match terminal::enable_raw_mode() {
            Result::Ok(_) => {
                Self {
                    last_key_pressed: KeyCode::Null,
                    last_modifiers: KeyModifiers::empty(),
                    last_char: None
                }
            }, 
            Err(e) => panic!("Failed to enable raw mode: {}", e)
        }
       
    }

    pub fn get_key(&mut self) -> std::io::Result<KeyEvent> {
        if event::poll(std::time::Duration::from_millis(100))? {
            if let Event::Key(key_event) = event::read()? {
                // Store the key and modifiers for later use
                self.last_key_pressed = key_event.code;
                self.last_modifiers = key_event.modifiers;

                // Store the character if it's a Char key
                if let KeyCode::Char(c) = key_event.code {
                    self.last_char = Some(c);
                }

                return Ok(key_event);
            }
        }
        Ok(KeyEvent::new(KeyCode::Null, KeyModifiers::empty()))
    }

    // Get the current state of modifier keys
    pub fn get_modifier_state(&self) -> ModifierState {
        ModifierState {
            shift: self.last_modifiers.contains(KeyModifiers::SHIFT),
            ctrl: self.last_modifiers.contains(KeyModifiers::CONTROL),
            alt: self.last_modifiers.contains(KeyModifiers::ALT),
            meta: self.last_modifiers.contains(KeyModifiers::SUPER), // Command/Windows key
        }
    }

    // Get the last character that was pressed (if any)
    pub fn get_last_char(&self) -> Option<char> {
        self.last_char
    }
}
