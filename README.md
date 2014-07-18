# Alfred 2 workflow Delete Recent File

Recent file list is convenience function that let you open files quickly.
It's a nice feature, I agree. But if it gets you unsatisfied when there're unexpected items added to the list,
this tool may help you.

## Installation

You can download the Delete Recent File.alfredworkflow and import to Alfred 2.

Or you can `git clone` or download this repository.

## Usage
### 1.Trigger this workflow by typing the keyword `delrecent`.
> Feel free to change the keyword to whatever you like after importing this workflow:)

A list of apps which is keeping its own recent files is shown.

### 2. Type the application name .
After typing the trigger keyword, you have to **input the app name** whose recent file list you want to clear.
I know this is annoying, but I can't find way to auto-complete the app name by invoking Alfred's API.
I tried to do some fuzzy matching and hope it can make this step easier.

### 3. Select the item that you want to clear.
The last step is simple. You just select a item which you want to delete. Or if you prefer typing,
you can continue hitting keyboard just like step 2.



After the deletion, a notification will pop up to let you know things are done.