use console::{Key, Term};

pub(crate) struct Keyboard {
    last_key_pressed: Key,
    term: Term
}

impl Keyboard {
    pub fn new() -> Self {
        Self {
            last_key_pressed: Key::Unknown,
            term : Term::stdout()
        }
    }

    pub fn get_key(&self) -> std::io::Result<Key> {
        let key = self.term.read_key();
        key
    }
}