import tkinter
import requests
import pycountry
import os
from tkinter import messagebox
from settings import us_states

root = tkinter.Tk()
root.resizable(0, 0)
root.geometry("470x500")
root.iconbitmap("weather.ico")

URL = "https://api.openweathermap.org/data/2.5/weather"
lat_long_URL = "http://api.openweathermap.org/geo/1.0/direct"
ZIP_URL = "http://api.openweathermap.org/geo/1.0/zip"
KEY = os.environ.get('API_KEY')

def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_2
        else:
            return None
    except LookupError:
        return None

def get_state_code(state_name):
    try:
        us_subdivisions = pycountry.subdivisions.get(country_code='US')

        state = next((subdivision for subdivision in us_subdivisions if subdivision.name == state_name), None)

        if state:
            return state.code
        else:
            return None

    except LookupError:
        return None

def delete_all_labels():
    for widget in weather_label_frame.winfo_children():
        if isinstance(widget, tkinter.Label):
            widget.destroy()

def submit():
    try:
        if (entry.get() != "" and entry_country.get() != ""):
            if intvar.get() == 0:
                delete_all_labels()
                if entry.get().title() not in us_states:
                    params = {"appid": KEY, "q": f"{entry.get().title()},{get_country_code(entry_country.get().title())}"}
                else:
                    params = {"appid": KEY, "q": f"{entry.get().title()},{get_state_code(entry.get().title())},{get_country_code(entry_country.get().title())}"}
                response = requests.get(lat_long_URL, params=params)
                data = response.json()
                latitude = data[0]["lat"]
                longitude = data[0]["lon"]

                params2 = {"appid": KEY, "lat": latitude, "lon": longitude, "units": "metric"}
                response2 = requests.get(URL, params=params2)
                data2 = response2.json()

                city = tkinter.Label(weather_label_frame, text=f"{entry.get().title()}({data2['coord']['lat']}, {data2['coord']['lon']})", font=(12), bg="#d1f0ef")
                city.pack(pady=10)

                weather = tkinter.Label(weather_label_frame, text=f"Weather: {data2['weather'][0]['main']}, {data2['weather'][0]['description']}", bg="#d1f0ef")
                weather.pack(pady=2)

                temperature = tkinter.Label(weather_label_frame, text=f"Temperature: {data2['main']['temp']}°C", bg="#d1f0ef")
                temperature.pack(pady=2)

                feels_like = tkinter.Label(weather_label_frame, text=f"Feels Like: {data2['main']['feels_like']}°C", bg="#d1f0ef")
                feels_like.pack(pady=2)

                min_temp = tkinter.Label(weather_label_frame, text=f"Min Temperature: {data2['main']['temp_min']}°C", bg="#d1f0ef")
                min_temp.pack(pady=2)

                max_temp = tkinter.Label(weather_label_frame, text=f"Max Temperature: {data2['main']['temp_max']}°C", bg="#d1f0ef")
                max_temp.pack(pady=2)

                humidity = tkinter.Label(weather_label_frame, text=f"Humidity: {data2['main']['humidity']}", bg="#d1f0ef")
                humidity.pack(pady=2)
            else:
                delete_all_labels()
                params = {"zip": f"{entry.get()}", "appid": KEY}
                response = requests.get(ZIP_URL, params=params)
                data = response.json()
                latitude = data["lat"]
                longitude = data["lon"]
                city_name = data['name']

                params2 = {"lat": latitude, "lon":longitude, "appid": KEY, "units": "metric"}
                response2 = requests.get(URL, params=params2)
                data2 = response2.json()
                city = tkinter.Label(weather_label_frame,
                                     text=f"{data2['name']}({data2['coord']['lat']}, {data2['coord']['lon']})",
                                     font=(12), bg="#d1f0ef")
                city.pack(pady=10)

                weather = tkinter.Label(weather_label_frame,
                                        text=f"Weather: {data2['weather'][0]['main']}, {data2['weather'][0]['description']}",
                                        bg="#d1f0ef")
                weather.pack(pady=2)

                temperature = tkinter.Label(weather_label_frame, text=f"Temperature: {data2['main']['temp']}°C",
                                            bg="#d1f0ef")
                temperature.pack(pady=2)

                feels_like = tkinter.Label(weather_label_frame, text=f"Feels Like: {data2['main']['feels_like']}°C",
                                           bg="#d1f0ef")
                feels_like.pack(pady=2)

                min_temp = tkinter.Label(weather_label_frame, text=f"Min Temperature: {data2['main']['temp_min']}°C",
                                         bg="#d1f0ef")
                min_temp.pack(pady=2)

                max_temp = tkinter.Label(weather_label_frame, text=f"Max Temperature: {data2['main']['temp_max']}°C",
                                         bg="#d1f0ef")
                max_temp.pack(pady=2)

                humidity = tkinter.Label(weather_label_frame, text=f"Humidity: {data2['main']['humidity']}", bg="#d1f0ef")
                humidity.pack(pady=2)
        else:
            messagebox.showinfo(title="No blanks", message="dont leave any blanks!")


    except:
        delete_all_labels()
        word = tkinter.Label(weather_label_frame, text="that city does not exist!", bg="#d1f0ef", font=(12))
        word.pack(pady=10)


output_frame = tkinter.Frame(root, bg="#AEECEF", height=300)
input_frame = tkinter.Frame(root, bg="#53599A")
output_frame.pack(fill=tkinter.BOTH, expand=True)
input_frame.pack(fill=tkinter.BOTH, expand=False)

label_frame = tkinter.LabelFrame(input_frame, bg="#068D9D")
label_frame.pack(padx=10, pady=10, expand=True, fill=tkinter.BOTH)


city_name = tkinter.Label(label_frame, bg="#068D9D", text="City Name:")
city_name.grid(row=0, column=0, padx=10, pady=10, sticky="we")

entry = tkinter.Entry(label_frame, width=30)
entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

country_name = tkinter.Label(label_frame, text="Country Name:", bg="#068D9D")
country_name.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry_country = tkinter.Entry(label_frame, width=30)
entry_country.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

submit_button = tkinter.Button(label_frame, text="Submit", command=submit)
submit_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10,)

intvar = tkinter.IntVar()
intvar.set(0)

radiobutton1 = tkinter.Radiobutton(label_frame, text="Search by city name", variable=intvar, value=0, bg="#068D9D", activebackground="#068D9D")
radiobutton2 = tkinter.Radiobutton(label_frame, text="Search by zipcode", variable=intvar, value=1, bg="#068D9D", activebackground="#068D9D")

radiobutton1.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")
radiobutton2.grid(row=2, column=2, padx=10, pady=10, sticky="e")

weather_label_frame = tkinter.LabelFrame(output_frame, bg="#d1f0ef", height=280)
weather_label_frame.pack(expand=True, fill=tkinter.BOTH, padx=40, pady=40)

root.mainloop()