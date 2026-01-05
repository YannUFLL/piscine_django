from path import Path

def execute():
    try:
        p = Path('giga_chad')
        p.makedirs_p()
        file = p / "my_loved_file"
        file.write_text("\u266CCOUCOU_LES_CONGOLAIS\u266C")
        file_content = file.read_text()
        print(file_content)
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    execute()
