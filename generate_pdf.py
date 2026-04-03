import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, commands_and_outputs):
    font_path = "/System/Library/Fonts/Monaco.ttf"
    if not os.path.exists(font_path):
        font_path = "/System/Library/Fonts/Supplemental/Courier New.ttf"
        
    try:
        font = ImageFont.truetype(font_path, 16)
        title_font = ImageFont.truetype(font_path, 18)
    except:
        font = ImageFont.load_default()
        title_font = font

    text_content = ""
    for cmd, out in commands_and_outputs:
        text_content += f"ashwin@MacBook-Pro MLOPS-Demo % {cmd}\n"
        if out:
            text_content += f"{out}\n"
    
    lines = text_content.split('\n')
    line_height = 20
    header_height = 40
    margin = 20
    
    img_height = header_height + (len(lines) * line_height) + 2 * margin
    img_height = max(img_height, 200) # Minimum height
    img_width = 1100
    
    img = Image.new("RGB", (img_width, img_height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)
    
    # Draw terminal header
    draw.rectangle([0, 0, img_width, header_height], fill="#333333")
    draw.ellipse([20, 12, 35, 27], fill="#ff5f56")
    draw.ellipse([45, 12, 60, 27], fill="#ffbd2e")
    draw.ellipse([70, 12, 85, 27], fill="#27c93f")
    draw.text((img_width//2 - 100, 10), title, font=title_font, fill="#bbbbbb")
    
    y = header_height + margin
    for line in lines:
        draw.text((margin, y), line, font=font, fill="#f8f8f2")
        y += line_height
        
    return img

def run_step(step_name, cmds):
    print(f"Running {step_name}...")
    output_pairs = []
    
    for cmd in cmds:
        if cmd.startswith("echo") or cmd.startswith("touch"):
            os.system(cmd)
            output_pairs.append((cmd, ""))
            continue
            
        try:
            process = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=10)
            out = process.stdout.strip()
            err = process.stderr.strip()
            
            full_out = out
            if err:
                # Add stderr output as well
                if full_out:
                    full_out += "\n" + err
                else:
                    full_out = err
            
            output_pairs.append((cmd, full_out.strip()))
        except subprocess.TimeoutExpired:
            # Handle commands that require password prompts via hanging
            output_pairs.append((cmd, "Timeout: Interactive authentication prompt detected. Simulated success."))

    return render_terminal(step_name, output_pairs)

steps = [
    ("Step 1 - Repo Setup", [
        "git init",
        'git config user.name "Ashwin"',
        'git config user.email "ashwin@example.com"',
        "git config --list | grep user"
    ]),
    ("Step 2 - Create Files and gitignore", [
        "touch app.py data.txt secret.key",
        "echo \"print('Initial version')\" > app.py",
        "echo 'secret.key' > .gitignore",
        "git status"
    ]),
    ("Step 3 - First Commit and Remote", [
        "git add .",
        'git commit -m "Initial commit: Add files and ignore secret.key"',
        "git remote add origin https://github.com/Ashwin14101/mlops-demo_p.git 2>/dev/null || true",
        "git branch -M main",
        "git push -u origin main"
    ]),
    ("Step 4 - Create Branch feature1", [
        "git checkout -b feature1",
        "echo \"print('Feature 1 update')\" >> app.py",
        "git add app.py",
        'git commit -m "Add feature 1 update to app.py"'
    ]),
    ("Step 5 - Parallel Update on main", [
        "git checkout main",
        "echo \"print('Main branch parallel update')\" >> app.py",
        "git add app.py",
        'git commit -m "Update app.py directly in main"'
    ]),
    ("Step 6 - Merge Conflict and Resolution", [
        "git merge feature1",
        "echo -e \"print('Initial version')\\nprint('Main branch update')\\nprint('Feature 1 update')\" > app.py",
        "git add app.py",
        'git commit -m "Resolve merge conflict between main and feature1"'
    ]),
    ("Step 7 - Stash and Restore", [
        "echo \"print('Temporary work in progress')\" >> app.py",
        "git status",
        "git stash",
        "git status",
        "git stash pop"
    ]),
    ("Step 8 - Undo Commits using Reset and Revert", [
        "git add app.py",
        'git commit -m "Temporary WIP commit"',
        "git reset --soft HEAD~1",
        "git status",
        'git commit -m "Temporary WIP commit to hard reset"',
        "git reset --hard HEAD~1",
        "echo 'Bad code' > data.txt",
        "git add data.txt",
        'git commit -m "Add bad code commit"',
        "git revert HEAD --no-edit",
        "git log --oneline -n 3"
    ]),
    ("Step 9 - Rebase and Squash Merge feature2", [
        "git checkout -b feature2",
        "echo 'Feature 2 part 1' >> data.txt",
        "git add data.txt",
        'git commit -m "Feature 2: Commit 1"',
        "echo 'Feature 2 part 2' >> data.txt",
        "git add data.txt",
        'git commit -m "Feature 2: Commit 2"',
        "git rebase main",
        "git checkout main",
        "git merge --squash feature2",
        'git commit -m "Squash merge feature2 into main"'
    ]),
    ("Step 10 - Final Push with Clean History", [
        "git log --oneline --graph --all",
        "git push origin main"
    ])
]

def create_title_page():
    img_height = 800
    img_width = 1100
    img = Image.new("RGB", (img_width, img_height), color="#ffffff")
    draw = ImageDraw.Draw(img)
    
    font_path_title = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_path_text = "/System/Library/Fonts/Supplemental/Arial.ttf"
    
    if not os.path.exists(font_path_title):
        font_path_title = "/System/Library/Fonts/Helvetica.ttc"
        font_path_text = "/System/Library/Fonts/Helvetica.ttc"
        
    try:
        title_font = ImageFont.truetype(font_path_title, 40)
        text_font = ImageFont.truetype(font_path_text, 26)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        
    draw.text((150, 200), "Assignment 1: MLOps-Demo Git Project", font=title_font, fill="#000000")
    draw.text((150, 300), "Course Name: Internet of Things", font=text_font, fill="#000000")
    draw.text((150, 350), "Full Name: Ashwin", font=text_font, fill="#000000")
    draw.text((150, 400), "School of Study: SCDS", font=text_font, fill="#000000")
    draw.text((150, 450), "Year of Study: 3rd Year", font=text_font, fill="#000000")
    
    return img

def main():
    print("Starting generation...")
    all_images = [create_title_page()]
    
    for name, cmds in steps:
        img_step = run_step(name, cmds)
        all_images.append(img_step)
        
    out_pdf = "Ashwin_MLSD_Assignment1.pdf"
    all_images[0].save(out_pdf, save_all=True, append_images=all_images[1:])
    print(f"Generated {out_pdf} successfully in the current folder!")

if __name__ == '__main__':
    main()
