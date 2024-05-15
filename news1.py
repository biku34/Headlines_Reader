import tkinter as tk
from PIL import Image, ImageTk
import pyfiglet
import requests
from bs4 import BeautifulSoup
import webbrowser
import pyttsx3

ascii_banner = pyfiglet.figlet_format("T o d a y 's N e w s", font='standard')

root = tk.Tk()
root.title("News Reader")
root.geometry("1000x1000")

image = Image.open("bg.png")
photo = ImageTk.PhotoImage(image)

label = tk.Label(root, text=ascii_banner, font=("Courier", 10))
label.pack(pady=10)

label = tk.Label(root, text="----------------------------------------------------------------------------------------")
label.pack(pady=10)

label = tk.Label(root, text="Featuring your city's headlines from Times Now at one go", font=("Times New Roman", 18))
label.pack(pady=10)

image_label = tk.Label(root, image=photo)
image_label.pack(pady=10)

def button_click():
    urls = [
    'https://www.timesnownews.com/mumbai',
    'https://www.timesnownews.com/delhi',
    'https://www.timesnownews.com//kolkata',
    'https://www.timesnownews.com//bengaluru',
    'https://www.timesnownews.com//hyderabad',
    'https://www.timesnownews.com/chennai',
    'https://www.timesnownews.com/city/ahmedabad'
    ]

    def process_url(url):
        try:
            r = requests.get(url)
            r.raise_for_status()  
            htmlcontent = r.content

            soup = BeautifulSoup(htmlcontent, 'html.parser')

            anchors = soup.find_all('a')
            all_links = set()
            for link in anchors:
                href = link.get('href')
                if href and href != '#':
                    link_text = link.get_text().strip()
                    all_links.add(link_text)

            return all_links

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while processing {url}: {e}")
            return set()

    unique_headlines = set()

    for url in urls:
        headlines = process_url(url)
        unique_headlines.update(headlines)

    with open("example.txt", "w", encoding="utf-8") as file:
        for link in unique_headlines:
            if len(link) > 25:
                file.write(link + "\n")

    search_window = tk.Toplevel(root)
    search_window.title("Headlines!!")
    search_window.geometry("1000x1000")

    options = ["Kolkata", "Delhi", "Mumbai", "Chennai", "Bengaluru", "Hyderabad", "Ahmedabad"]
    selected_option = tk.StringVar()
    selected_option.set(options[0])
    
    label = tk.Label(search_window, text="Choose your city!", font=("Monotype Corsiva", 18))
    label.pack()
    
    label = tk.Label(search_window, text="----------------------------------------------------------------------------------------")
    label.pack(pady=10)

    radio_frame = tk.Frame(search_window)
    radio_frame.pack()

    for option in options:
        radio_button = tk.Radiobutton(radio_frame, text=option, variable=selected_option, value=option)
        radio_button.pack(side=tk.LEFT, padx=10)
    
    def read_headline_aloud(headline):
        engine = pyttsx3.init()
        engine.say(headline)
        webbrowser.open_new(headline)
        engine.runAndWait()

    def search_in_file():
        for widget in results_frame.winfo_children():
            widget.destroy()
        
        selected_string = selected_option.get()
        try:
            with open('example.txt', 'r', encoding='utf-8') as file:  
                found = False
                for line in file:
                    if selected_string in line:
                        found = True
                        result_label = tk.Label(results_frame, text=line.strip())
                        result_label.pack(anchor=tk.CENTER)
                        result_label.bind("<Button-1>", lambda e, h=line.strip(): read_headline_aloud(h))
                if not found:
                    result_label = tk.Label(results_frame, text="No matching line found.")
                    result_label.pack(anchor=tk.CENTER)
        except FileNotFoundError:
            result_label = tk.Label(results_frame, text="The file does not exist.")
            result_label.pack(anchor=tk.CENTER)

    search_button = tk.Button(search_window, text="Search", command=search_in_file)
    search_button.pack()

    results_frame = tk.Frame(search_window)
    results_frame.pack(fill=tk.BOTH, expand=True)

button = tk.Button(root, text="Check it Out!", command=button_click)
button.pack(pady=10)

label = tk.Label(root, text="PS : You can click on headlines to read the news in detail\n and also hear it", font=("Times New Roman", 14))
label.pack(pady=10)

label = tk.Label(root, text="Built by Bikram Sadhukhan", font=("Times New Roman", 12))
label.pack(pady=50)

root.mainloop()
