import tkinter as tk
from tkinter import messagebox, ttk
import csv

class ProductForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario de Productos")

        # Definir las categorías permitidas
        self.allowed_categories = ["Chocolates", "Caramelos", "Mashmelos", "Galletas", "Salados", "Gomas de mascar"]

        # Lista para almacenar los productos
        self.products = []

        # Crear los elementos del formulario
        self.create_widgets()

    def create_widgets(self):
        # Nombre del producto
        tk.Label(self.root, text="Nombre del Producto:").grid(row=0, column=0, sticky=tk.W)
        self.product_name = tk.Entry(self.root, width=30)
        self.product_name.grid(row=0, column=1)

        # Precio del producto
        tk.Label(self.root, text="Precio del Producto:").grid(row=1, column=0, sticky=tk.W)
        self.product_price = tk.Entry(self.root, width=30)
        self.product_price.grid(row=1, column=1)

        # Categorías del producto
        tk.Label(self.root, text="Categorías del Producto:").grid(row=2, column=0, sticky=tk.W)
        self.categories_vars = {}
        for idx, category in enumerate(self.allowed_categories):
            var = tk.StringVar()
            chk = tk.Checkbutton(self.root, text=category, variable=var, onvalue=category, offvalue="")
            chk.grid(row=2+idx, column=1, sticky=tk.W)
            self.categories_vars[category] = var

        # Estado del producto en venta
        tk.Label(self.root, text="¿El Producto está en Venta?:").grid(row=2+len(self.allowed_categories), column=0, sticky=tk.W)
        self.sale_status = tk.StringVar()
        ttk.Radiobutton(self.root, text='Sí', value='Sí', variable=self.sale_status).grid(row=2+len(self.allowed_categories), column=1, sticky=tk.W)
        ttk.Radiobutton(self.root, text='No', value='No', variable=self.sale_status).grid(row=2+len(self.allowed_categories)+1, column=1, sticky=tk.W)

        # Botón de envío
        self.submit_button = ttk.Button(self.root, text="Enviar", command=self.validate_form)
        self.submit_button.grid(row=3+len(self.allowed_categories)+1, column=1)

        # Botón para guardar en archivo CSV
        self.save_button = ttk.Button(self.root, text="Guardar en CSV", command=self.save_to_csv)
        self.save_button.grid(row=4+len(self.allowed_categories)+1, column=1)

    def validate_form(self):
        try:
            # Validar el nombre del producto
            product_name = self.product_name.get()
            if len(product_name) > 20:
                raise ValueError("El nombre del producto no debe ser mayor a 20 caracteres.")

            # Validar el precio del producto
            product_price = float(self.product_price.get())
            if product_price <= 0 or product_price >= 999:
                raise ValueError("El precio del producto debe ser mayor a 0 y menor a 999 soles.")
            
            # Validar las categorías seleccionadas
            selected_categories = [var.get() for var in self.categories_vars.values() if var.get()]
            for category in selected_categories:
                if category not in self.allowed_categories:
                    raise ValueError("Categoría seleccionada no es válida.")
            if not selected_categories:
                raise ValueError("Debe seleccionar al menos una categoría.")

            # Validar el estado de venta del producto
            sale_status = self.sale_status.get()
            if sale_status not in ["Sí", "No"]:
                raise ValueError("Debe definir si el producto está en venta o no.")

            # Si todas las validaciones son correctas, agregar el producto a la lista
            self.products.append({
                "Nombre": product_name,
                "Precio": product_price,
                "Categorías": ", ".join(selected_categories),
                "En venta": sale_status
            })
            messagebox.showinfo("Éxito", "Felicidades, su producto se agregó.")
        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Lo sentimos, no pudo crear este producto.\n{e}")
        except Exception as e:
            messagebox.showerror("Error", "Por favor verifique el campo del precio.")

    def save_to_csv(self):
        # Guardar los productos en un archivo CSV
        with open('productos.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Nombre", "Precio", "Categorías", "En venta"])
            writer.writeheader()
            for product in self.products:
                writer.writerow(product)
        messagebox.showinfo("Guardado", "Los productos se guardaron en 'productos.csv'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductForm(root)
    root.mainloop()
