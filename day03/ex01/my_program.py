from path import Path



def execute():
    p = Path('giga_chad')
    p.makedirs_p()
    file = p / "my_loved_file"
    file.write_text("\u266CCOUCOU_LES_CONGOLAIS\u266C")

if __name__ == "__main__":
    execute()
