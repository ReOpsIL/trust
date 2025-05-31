#[derive(Debug, Clone)]
pub struct TextBuffer {
    lines: Vec<String>,
    //selected_lines: Vec<String>,
    cursor_line: usize, // 0-indexed line number
    cursor_col: usize,  // 0-indexed character column in the current line
    clipboard: Option<Vec<String>>, // For cut/copy/paste - stores lines
    tab_width: usize,
}

impl TextBuffer {
    pub fn new() -> Self {
        TextBuffer {
            lines: vec![String::new()], // Start with one empty line
            //selected_lines: vec![String::new()], // Start with one empty line
            cursor_line: 0,
            cursor_col: 0,
            clipboard: None,
            tab_width: 4, // Default tab width
        }
    }

    // --- Cursor Management ---
    pub fn move_cursor(&mut self, line: usize, col: usize) {
        if line < self.lines.len() {
            self.cursor_line = line;
            let current_line_len = self.lines[self.cursor_line].chars().count();
            self.cursor_col = col.min(current_line_len);
        }
        // Optionally, handle out-of-bounds gracefully or panic/error
    }

    pub fn undo(&mut self) {
        
    }
    pub fn redo(&mut self) {

    }
    pub fn select_all(&mut self) {
        
    }
    pub fn select_word_left(&mut self) {
        let current_line = &self.lines[self.cursor_line];
        let chars: Vec<char> = current_line.chars().collect();

        // If cursor is at the start of the line, no word to select
        if self.cursor_col == 0 {
            //self.selected_lines = vec![String::new()];
            return;
        }

        // Find the start of the word to the left
        let mut start_col = self.cursor_col;
        let mut end_col = self.cursor_col;

        // Move backwards to find the start of the word
        while start_col > 0 && !chars[start_col - 1].is_whitespace() {
            start_col -= 1;
        }

        // Extract the selected word
        let selected_text: String = chars[start_col..end_col].iter().collect();
        //self.selected_lines = vec![selected_text.clone()];

        // Update cursor to the start of the selected word
        self.cursor_col = start_col;

        // Store in clipboard for potential copy/paste
        self.clipboard = Some(vec![selected_text]);
    }


    // Select the word to the right of the cursor
    pub fn select_word_right(&mut self) {
        let current_line = &self.lines[self.cursor_line];
        let chars: Vec<char> = current_line.chars().collect();
        let line_len = chars.len();

        // If cursor is at the end of the line, no word to select
        if self.cursor_col >= line_len {
            //self.selected_lines = vec![String::new()];
            return;
        }

        // Find the end of the word to the right
        let mut start_col = self.cursor_col;
        let mut end_col = self.cursor_col;

        // Move forward to find the end of the word
        while end_col < line_len && !chars[end_col].is_whitespace() {
            end_col += 1;
        }

        // Extract the selected word
        let selected_text: String = chars[start_col..end_col].iter().collect();
        //self.selected_lines = vec![selected_text.clone()];

        // Update cursor to the end of the selected word
        self.cursor_col = end_col;

        // Store in clipboard for potential copy/paste
        self.clipboard = Some(vec![selected_text]);
    }

    pub fn select_char_left(&mut self) {
        let current_line = &self.lines[self.cursor_line];
        let chars: Vec<char> = current_line.chars().collect();

        // If cursor is at the start of the line, nothing to select
        if self.cursor_col == 0 {
            //self.selected_lines = vec![String::new()];
            return;
        }

        // Select the character immediately to the left
        let selected_char = chars[self.cursor_col - 1];
        //self.selected_lines = vec![selected_char.to_string()];

        // Move cursor left
        self.cursor_col -= 1;

        // Store in clipboard
        self.clipboard = Some(vec![selected_char.to_string()]);
    }

    // Select the character to the right of the cursor
    pub fn select_char_right(&mut self) {
        let current_line = &self.lines[self.cursor_line];
        let chars: Vec<char> = current_line.chars().collect();
        let line_len = chars.len();

        // If cursor is at the end of the line, nothing to select
        if self.cursor_col >= line_len {
            //self.selected_lines = vec![String::new()];
            return;
        }

        // Select the character at the cursor
        let selected_char = chars[self.cursor_col];
        //self.selected_lines = vec![selected_char.to_string()];

        // Move cursor right
        self.cursor_col += 1;

        // Store in clipboard
        self.clipboard = Some(vec![selected_char.to_string()]);
    }

    pub fn select_line_down(&mut self) {
        if self.cursor_line < self.lines.len() - 1 {
            self.cursor_line += 1;
        }
    }
    pub fn select_line_up(&mut self) {
        if self.cursor_line > 0 {
            self.cursor_line -= 1;
        }
    }
    pub fn select_line_to_end(&mut self) {
        self.cursor_line = self.lines.len() - 1;
    }
    pub fn select_line_to_start(&mut self) {
        self.cursor_line = 0;
    }
    pub fn move_cursor_up(&mut self) {
        if self.cursor_line > 0 {
            self.cursor_line -= 1;
            // Adjust column to be within the new line's bounds
            let current_line_len = self.lines[self.cursor_line].chars().count();
            self.cursor_col = self.cursor_col.min(current_line_len);
        }
    }

    pub fn move_cursor_down(&mut self) {
        if self.cursor_line < self.lines.len() - 1 {
            self.cursor_line += 1;
            // Adjust column to be within the new line's bounds
            let current_line_len = self.lines[self.cursor_line].chars().count();
            self.cursor_col = self.cursor_col.min(current_line_len);
        }
    }

    pub fn move_cursor_left(&mut self) {
        if self.cursor_col > 0 {
            self.cursor_col -= 1;
        } else if self.cursor_line > 0 {
            // Move to end of previous line
            self.cursor_line -= 1;
            self.cursor_col = self.lines[self.cursor_line].chars().count();
        }
    }

    pub fn move_cursor_right(&mut self) {
        let current_line_len = self.lines[self.cursor_line].chars().count();
        if self.cursor_col < current_line_len {
            self.cursor_col += 1;
        } else if self.cursor_line < self.lines.len() - 1 {
            // Move to start of next line
            self.cursor_line += 1;
            self.cursor_col = 0;
        }
    }
    pub fn move_cursor_to_beginning_of_line(&mut self) {
        self.cursor_col = 0;
    }

    pub fn move_cursor_to_end_of_line(&mut self) {
        let current_line_len = self.lines[self.cursor_line].chars().count();
        self.cursor_col = current_line_len;
    }

    // --- Basic Editing ---
    pub fn insert_char(&mut self, ch: char) {
        if ch == '\n' {
            self.insert_newline();
        } else {
            let current_line = &mut self.lines[self.cursor_line];
            // Ensure cursor_col is valid for byte indexing if using insert
            // It's safer to collect to Vec<char> for manipulation if complex
            // Or, find the byte index for the char index
            let mut byte_idx = 0;
            for (i, c) in current_line.char_indices() {
                if i == self.cursor_col { // This is incorrect, should be char count
                    byte_idx = i;
                    break;
                }
                if i > self.cursor_col { // Should not happen if cursor_col is char index
                    byte_idx = current_line.len(); // append
                    break;
                }
            }
            // Correct way to find byte_idx from char_idx (cursor_col)
            let byte_idx = current_line.char_indices()
                .nth(self.cursor_col)
                .map_or(current_line.len(), |(idx, _)| idx);

            current_line.insert(byte_idx, ch);
            self.cursor_col += 1;
        }
    }

    pub fn insert_str(&mut self, text: &str) {
        // This could be smarter and handle embedded newlines in `text`
        for ch in text.chars() {
            self.insert_char(ch); // Leverages existing newline logic
        }
    }

    pub fn insert_newline(&mut self) {
        let current_line_content = self.lines[self.cursor_line].clone();

        let (before_cursor, after_cursor) = current_line_content.char_indices().nth(self.cursor_col)
            .map_or((current_line_content.as_str(), ""), |(byte_idx, _)| {
                current_line_content.split_at(byte_idx)
            });

        self.lines[self.cursor_line] = String::from(before_cursor);
        self.lines.insert(self.cursor_line + 1, String::from(after_cursor));

        self.cursor_line += 1;
        self.cursor_col = 0;
    }

    pub fn delete_char_before_cursor(&mut self) { // Backspace
        if self.cursor_col > 0 {
            let current_line = &mut self.lines[self.cursor_line];
            // Find byte index for char removal
            let byte_idx_to_remove = current_line.char_indices()
                .nth(self.cursor_col -1) // char before cursor
                .map(|(idx, _)| idx)
                .unwrap_or(0); // Should always find one if cursor_col > 0

            current_line.remove(byte_idx_to_remove);
            self.cursor_col -= 1;
        } else if self.cursor_line > 0 { // At the beginning of a line, not the first line
            let line_to_merge = self.lines.remove(self.cursor_line);
            self.cursor_line -= 1;
            self.cursor_col = self.lines[self.cursor_line].chars().count();
            self.lines[self.cursor_line].push_str(&line_to_merge);
        }
    }

    pub fn delete_char_at_cursor(&mut self) { // Delete
        let current_line_len_chars = self.lines[self.cursor_line].chars().count();
        if self.cursor_col < current_line_len_chars {
            let current_line = &mut self.lines[self.cursor_line];
            // Find byte index for char removal
            let byte_idx_to_remove = current_line.char_indices()
                .nth(self.cursor_col)
                .map(|(idx, _)| idx)
                .unwrap_or(0); // Should always find one

            current_line.remove(byte_idx_to_remove);
            // Cursor column doesn't change
        } else if self.cursor_col == current_line_len_chars && self.cursor_line < self.lines.len() - 1 {
            // At the end of a line, not the last line
            let next_line_content = self.lines.remove(self.cursor_line + 1);
            self.lines[self.cursor_line].push_str(&next_line_content);
            // Cursor column doesn't change, still at end of merged line
        }
    }

    // --- Cut, Copy, Paste (Line-based for simplicity here) ---
    // For character-level selection, you'd need start_line, start_col, end_line, end_col
    pub fn cut_current_line(&mut self) {
        if !self.lines.is_empty() {
            let cut_line_content = self.lines.remove(self.cursor_line);
            self.clipboard = Some(vec![cut_line_content]);

            if self.lines.is_empty() { // If we removed the last line
                self.lines.push(String::new()); // Add an empty line back
                self.cursor_line = 0;
            } else if self.cursor_line >= self.lines.len() { // If cursor was on the last line
                self.cursor_line = self.lines.len() - 1;
            }
            // Adjust cursor column to be within the new current line's bounds
            let current_line_len = self.lines[self.cursor_line].chars().count();
            self.cursor_col = self.cursor_col.min(current_line_len);
        }
    }

    // A more general cut (example: cut lines from start_idx to end_idx inclusive)
    pub fn cut_lines(&mut self, start_line_idx: usize, end_line_idx: usize) {
        if start_line_idx > end_line_idx || end_line_idx >= self.lines.len() {
            return; // Invalid range
        }
        let mut cut_lines_vec = Vec::new();
        for i in (start_line_idx..=end_line_idx).rev() { // Remove from back to front
            cut_lines_vec.insert(0, self.lines.remove(i));
        }
        self.clipboard = Some(cut_lines_vec);

        if self.lines.is_empty() {
            self.lines.push(String::new());
            self.cursor_line = 0;
            self.cursor_col = 0;
        } else {
            // Adjust cursor if it was in or after the cut region
            if self.cursor_line > end_line_idx {
                self.cursor_line -= (end_line_idx - start_line_idx + 1);
            } else if self.cursor_line >= start_line_idx {
                self.cursor_line = start_line_idx.min(self.lines.len() - 1);
            }
            let current_line_len = self.lines[self.cursor_line].chars().count();
            self.cursor_col = self.cursor_col.min(current_line_len);
        }
    }


    pub fn cut_selected_text(&mut self) {
    }
    
    pub fn copy_selected_text(&mut self) {
        if let Some(lines_to_copy) = &self.clipboard {
            if lines_to_copy.is_empty() {
                return;
            }
        }
    }
    pub fn copy_current_line(&mut self) {
        if !self.lines.is_empty() {
            self.clipboard = Some(vec![self.lines[self.cursor_line].clone()]);
        }
    }


    pub fn paste(&mut self) {
        if let Some(lines_to_paste) = &self.clipboard {
            if lines_to_paste.is_empty() {
                return;
            }

            let first_pasted_line = &lines_to_paste[0];
            let rest_of_pasted_lines = &lines_to_paste[1..];

            // Split current line at cursor
            let current_line_content = self.lines[self.cursor_line].clone();
            let byte_idx_at_cursor = current_line_content.char_indices()
                .nth(self.cursor_col)
                .map_or(current_line_content.len(), |(idx, _)| idx);

            let (before_cursor, after_cursor) = current_line_content.split_at(byte_idx_at_cursor);

            // Modify current line with first part of paste
            let mut new_current_line = String::from(before_cursor);
            new_current_line.push_str(first_pasted_line);

            let original_cursor_line = self.cursor_line;
            let new_cursor_col: usize;

            if rest_of_pasted_lines.is_empty() { // Single line paste
                new_current_line.push_str(after_cursor);
                self.lines[self.cursor_line] = new_current_line;
                new_cursor_col = (String::from(before_cursor) + first_pasted_line).chars().count();
            } else { // Multi-line paste
                self.lines[self.cursor_line] = new_current_line; // First pasted line part

                // Insert subsequent full lines from the clipboard
                for (i, line) in rest_of_pasted_lines.iter().enumerate() {
                    self.lines.insert(self.cursor_line + 1 + i, line.clone());
                }

                // Append the rest of the original line to the last pasted line
                let last_pasted_line_idx = self.cursor_line + rest_of_pasted_lines.len();
                self.lines[last_pasted_line_idx].push_str(after_cursor);

                self.cursor_line = last_pasted_line_idx;
                new_cursor_col = self.lines[last_pasted_line_idx].chars().count() - after_cursor.chars().count();
            }
            self.cursor_col = new_cursor_col;

        }
    }

    // --- Indentation ---
    pub fn indent_current_line(&mut self) { // Tab-push
        let spaces = " ".repeat(self.tab_width);
        self.lines[self.cursor_line].insert_str(0, &spaces);
        // If cursor was at col 0, it's now after the indent. Otherwise, it shifts.
        self.cursor_col += self.tab_width;
    }

    pub fn unindent_current_line(&mut self) { // Shift-Tab (conceptual)
        let current_line = &mut self.lines[self.cursor_line];
        let mut chars_removed = 0;
        for _ in 0..self.tab_width {
            if current_line.starts_with(' ') {
                current_line.remove(0);
                chars_removed += 1;
            } else {
                break; // Stop if non-space found or line is empty
            }
        }
        if self.cursor_col >= chars_removed {
            self.cursor_col -= chars_removed;
        } else {
            self.cursor_col = 0;
        }
    }

    // Indent a block of lines
    pub fn indent_lines(&mut self, start_line_idx: usize, end_line_idx: usize) {
        let spaces = " ".repeat(self.tab_width);
        for i in start_line_idx..=end_line_idx.min(self.lines.len() - 1) {
            self.lines[i].insert_str(0, &spaces);
            if i == self.cursor_line && self.cursor_col > 0 { // Don't adjust if cursor is at col 0
                self.cursor_col += self.tab_width;
            } else if i == self.cursor_line && self.cursor_col == 0 {
                // If cursor is at column 0 of an indented line, it moves by tab_width
                self.cursor_col += self.tab_width;
            }
        }
    }

    // --- Utility ---
    pub fn set_tab_width(&mut self, width: usize) {
        if width > 0 {
            self.tab_width = width;
        }
    }

    pub fn get_line_count(&self) -> usize {
        self.lines.len()
    }

    pub fn get_line(&self, line_num: usize) -> Option<&String> {
        self.lines.get(line_num)
    }

    pub fn get_cursor_line(&self) -> usize {
        self.cursor_line
    }

    pub fn get_cursor_col(&self) -> usize {
        self.cursor_col
    }

    pub fn get_buffer_content(&self) -> String {
        let mut buffer_content = String::new();
        for line in &self.lines {
            buffer_content.push_str(line);
            buffer_content.push('\n');
        }
        buffer_content
    }
    pub fn display(&self) {
        println!("--- Buffer Content (Cursor L:{}, C:{}) ---", self.cursor_line, self.cursor_col);
        for (i, line) in self.lines.iter().enumerate() {
            print!("{:3}: ", i); // Line number
            if i == self.cursor_line {
                // Show cursor position within the line for clarity
                let mut displayed_line = String::new();
                for (char_idx, ch) in line.chars().enumerate() {
                    if char_idx == self.cursor_col {
                        displayed_line.push('|'); // Cursor marker
                    }
                    displayed_line.push(ch);
                }
                if self.cursor_col == line.chars().count() { // Cursor at end of line
                    displayed_line.push('|');
                }
                println!("{}", displayed_line);
            } else {
                println!("{}", line);
            }
        }
        println!("------------------------------------");
        if let Some(clip_content) = &self.clipboard {
            println!("Clipboard: {:?}", clip_content);
        } else {
            println!("Clipboard: (empty)");
        }
        println!("------------------------------------");

    }
}
