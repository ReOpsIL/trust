use std::io::{self, Write};
use crossterm::{
    event::KeyCode,
    terminal::{self, Clear, ClearType},
    cursor::{self, SetCursorStyle},
    style::{self, Stylize},
    QueueableCommand, ExecutableCommand,
};

pub struct Printer {
    last_key: KeyCode,
    viewport_start: usize,  // First line to display
    viewport_height: usize, // Number of lines to display
}

impl Printer {
    pub fn new() -> Self {
        // Get terminal size to determine viewport height
        let (_, height) = terminal::size().unwrap_or((80, 24));

        Self {
            last_key: KeyCode::Null,
            viewport_start: 0,
            viewport_height: height as usize - 2, // Leave some space for status line
        }
    }

    pub fn clear_screen(&mut self) {
        let mut stdout = io::stdout();
        let _ = stdout.execute(Clear(ClearType::All));
        let _ = stdout.execute(cursor::MoveTo(0, 0));
    }

    pub fn print_buffer(&mut self, text: String, cursor_line: usize, cursor_col: usize) {
        let mut stdout = io::stdout();
        let _ = stdout.execute(Clear(ClearType::All));
        let _ = stdout.execute(cursor::MoveTo(0, 0));

        // Enable blinking cursor
        let _ = stdout.queue(SetCursorStyle::BlinkingBlock);

        // Split the text into lines
        let lines: Vec<&str> = text.lines().collect();

        // Calculate the visible range
        let total_lines = lines.len();
        let end_line = (self.viewport_start + self.viewport_height).min(total_lines);

        // Print only the visible lines
        for (i, line) in lines.iter().enumerate().skip(self.viewport_start).take(end_line - self.viewport_start) {
            let _ = stdout.queue(cursor::MoveTo(0, (i - self.viewport_start) as u16));
            let _ = stdout.queue(style::Print(line));
            let _ = stdout.queue(style::Print("\r\n"));
        }

        // Print status line
        let _ = stdout.queue(cursor::MoveTo(0, self.viewport_height as u16));
        let _ = stdout.queue(style::Print(format!("Lines {}-{} of {} (Viewport: {})", 
            self.viewport_start + 1, end_line, total_lines, self.viewport_height)));

        // Position cursor at the correct location (if visible)
        if cursor_line >= self.viewport_start && cursor_line < self.viewport_start + self.viewport_height {
            let visible_line = cursor_line - self.viewport_start;
            let _ = stdout.queue(cursor::MoveTo(cursor_col as u16, visible_line as u16));
        }

        let _ = stdout.flush();
    }

    pub fn scroll_up(&mut self) {
        if self.viewport_start > 0 {
            self.viewport_start -= 1;
        }
    }

    pub fn scroll_down(&mut self, total_lines: usize) {
        if self.viewport_start + self.viewport_height < total_lines {
            self.viewport_start += 1;
        }
    }

    pub fn set_viewport_start(&mut self, line: usize) {
        self.viewport_start = line;
    }

    pub fn get_viewport_start(&self) -> usize {
        self.viewport_start
    }

    pub fn get_viewport_height(&self) -> usize {
        self.viewport_height
    }

    pub fn print(&mut self, key: KeyCode) {
        self.last_key = key;
        let mut stdout = io::stdout();

        match self.last_key {
            KeyCode::Char(c) => {
                let _ = stdout.queue(style::Print(c));
            },
            KeyCode::Enter => {
                let _ = stdout.queue(style::Print("\r\n"));
            }
            _ => {}
        }

        let _ = stdout.flush();
    }
}
