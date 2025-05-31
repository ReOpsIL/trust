use crate::editor::app::App;
mod editor;

fn main() {
    
    let mut app: App = App::new();
    app.run();
    // 
    // let term = Term::stdout();
    // let key = term.read_key();
    // println!("{:?}", key);
}
