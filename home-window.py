import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import yaml
from ttkbootstrap import Style

import open_api_generator
import source_generator
from merging_apis import load_yaml, save_yaml, merge_yaml  # Import the yaml_merger module


class SwaggerConverterApp:
    def __init__(self, root):
        self.root = root
        self.script_version = 1.0

        # Use ttkbootstrap for a modern look
        style = Style(theme='flatly')
        root.title("Swagger Converter")
        root.geometry("700x700")
        root.configure(bg='#ffffff')

        # Main container with soft padding
        self.main_frame = tk.Frame(root, bg='#f4f6f9')
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Header
        self.header_label = tk.Label(
            self.main_frame,
            text="Swagger Converter v" + str(self.script_version),
            font=('Segoe UI', 20, 'bold'),
            bg='#f4f6f9',
            fg='#2c3e50'
        )
        self.header_label.pack(pady=(0, 20))

        # File Selection
        self.file_frame = tk.Frame(self.main_frame, bg='#f4f6f9')
        self.file_frame.pack(fill=tk.X, pady=10)

        self.file_label = tk.Label(
            self.file_frame,
            text="Select File",
            font=('Segoe UI', 12),
            bg='#f4f6f9',
            fg='#34495e'
        )
        self.file_label.pack(side=tk.LEFT)

        self.file_entry = ttk.Entry(self.file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)

        self.browse_button = ttk.Button(
            self.file_frame,
            text="Browse",
            command=self.select_file,
            style='primary.TButton'
        )
        self.browse_button.pack(side=tk.LEFT)

        # Conversion Options
        self.options = [
            "Convert JSON to YAML",
            "Convert YAML to JSON",
            "Generate OpenAPI YAML",
            "Generate Gateway YAML",
            "Generate Both YAMLs",
            "Merge YAML Files"  # New option for merging YAML files
        ]

        self.option_var = tk.StringVar(value="Select Conversion Type")
        self.option_menu = ttk.Combobox(
            self.main_frame,
            textvariable=self.option_var,
            values=self.options,
            state="readonly"
        )
        self.option_menu.pack(fill=tk.X, pady=10)
        self.option_menu.bind('<<ComboboxSelected>>', self.toggle_gateway_fields)

        # Gateway Fields Container
        self.gateway_frame = tk.Frame(self.main_frame, bg='#f4f6f9')
        self.gateway_frame.pack(fill=tk.X, pady=10)

        # Label, attribute_normalized_name, is_mandatory flag
        self.gateway_fields = [
            ("Frontend URL", "frontend_url", True),
            ("VPC Connection ID", "vpc_connection_id", True),
            ("Info Title", "info_title", True),
            ("Info Description", "info_description", False),
            ("Info Version", "info_version", True),
            ("Servers URL", "servers_url", True),
            ("Base Path Default", "base_path_default", True)
        ]

        self.gateway_entries = {}

        for label, attr, is_mandatory in self.gateway_fields:
            field_frame = tk.Frame(self.gateway_frame, bg='#f4f6f9')
            field_frame.pack(fill=tk.X, pady=5)

            tk.Label(
                field_frame,
                text=label + "*" if is_mandatory else label,
                font=('Segoe UI', 10),
                bg='#f4f6f9',
                fg='#34495e'
            ).pack(side=tk.LEFT)

            entry = ttk.Entry(field_frame, width=50, state='disabled')
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)

            self.gateway_entries[attr] = entry

        # Buttons to load and save gateway fields
        self.gateway_buttons_frame = tk.Frame(self.gateway_frame, bg='#f4f6f9')
        self.gateway_buttons_frame.pack(fill=tk.X, pady=5)

        self.load_gateway_button = ttk.Button(
            self.gateway_buttons_frame,
            text="Load Gateway Fields",
            command=self.load_gateway_fields_data,
            style='secondary.TButton'
        )
        self.load_gateway_button.pack(side=tk.LEFT, padx=5)

        self.save_gateway_button = ttk.Button(
            self.gateway_buttons_frame,
            text="Save Gateway Fields",
            command=self.save_gateway_fields_data,
            style='secondary.TButton'
        )
        self.save_gateway_button.pack(side=tk.LEFT, padx=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            style='primary.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(pady=10)

        # Run Button
        self.run_button = ttk.Button(
            self.main_frame,
            text="Convert",
            command=self.run_conversion,
            style='primary.TButton'
        )
        self.run_button.pack(pady=10)

        # Initially hide gateway fields
        self.toggle_gateway_fields()

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("YAML files", ["*.yaml", "*.yml"]), ("JSON files", "*.json")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def toggle_gateway_fields(self, event=None):
        selected_option = self.option_var.get()
        gateway_options = ["Generate Gateway YAML", "Generate Both YAMLs"]

        state = 'normal' if selected_option in gateway_options else 'disabled'
        for entry in self.gateway_entries.values():
            entry.config(state=state)

    def load_gateway_fields_data(self):
        """Load gateway fields from a JSON file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Load Gateway Fields"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                saved_data_script_version = data.get("version", 1.0) # to be used in the future for compatibility
                if saved_data_script_version != self.script_version:
                    raise Exception("Unsupported version of file saving/loading")
                fields_data = data.get("data", {})
                gateway_fields_data = fields_data.get("gatewayFields", {})
                # Update each gateway entry. Temporarily enable if necessary.
                for key, entry in self.gateway_entries.items():
                    # If the entry is disabled, temporarily enable it to update the value.
                    current_state = entry.cget('state')
                    if current_state == 'disabled':
                        entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.insert(0, gateway_fields_data.get(key, ""))
                    # Restore the state based on conversion option.
                self.toggle_gateway_fields()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load gateway fields: {e}")

    def save_gateway_fields_data(self):
        """Save current gateway fields to a JSON file."""
        script_version = 1.0 # To be changed if the structure of loading and saving change to allow compatibility
        data = {
            "version": script_version,
            "data": {
                "gatewayFields": {key: entry.get() for key, entry in self.gateway_entries.items()}
            }
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Gateway Fields"
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Success", "Gateway fields saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save gateway fields: {e}")

    def run_conversion(self):
        # Validate inputs
        if not self.file_entry.get():
            messagebox.showerror("Error", "Please select a file")
            return

        if self.option_var.get() == "Select Conversion Type":
            messagebox.showerror("Error", "Please select a conversion type")
            return

        # Reset progress bar
        self.progress_var.set(0)

        # Determine option index
        option_index = self.options.index(self.option_var.get()) + 1
        file_path = self.file_entry.get()

        try:
            # Determine output file path
            if option_index in [1, 2]:  # JSON to YAML or YAML to JSON
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".yml" if option_index == 1 else ".json",
                    filetypes=[("YAML files", "*.yml")] if option_index == 1 else [("JSON files", "*.json")]
                )
                if not output_file:
                    return

                if option_index == 1:  # JSON to YAML
                    self._convert_json_to_yaml(file_path, output_file)
                else:  # YAML to JSON
                    self._convert_yaml_to_json(file_path, output_file)

            elif option_index in [3, 4, 5]:  # OpenAPI or Gateway or Both
                # For gateway generation (options 4 and 5), validate mandatory fields
                # Removed "info_description" from the list as it is optional.
                gateway_options = [4, 5]
                if option_index in gateway_options:
                    # Check if gateway fields are filled
                    if not all(
                            self.gateway_entries[field].get() for field in
                            [attribute_name for _,attribute_name, is_mandatory in self.gateway_fields if is_mandatory]
                            ):
                        messagebox.showerror("Error", "Please fill in all mandatory gateway fields")
                        return

                # OpenAPI generation
                if option_index in [3, 5]:
                    openapi_file = filedialog.asksaveasfilename(
                        defaultextension=".yml",
                        filetypes=[("YAML files", "*.yml")]
                    )
                    if openapi_file:
                        open_api_generator.process_swagger_file(file_path, openapi_file)

                # Gateway generation
                if option_index in [4, 5]:
                    gateway_file = filedialog.asksaveasfilename(
                        defaultextension=".yml",
                        filetypes=[("YAML files", "*.yml")]
                    )
                    if gateway_file:
                        source_generator.format_swagger_to_template(
                            file_path,
                            gateway_file,
                            self.gateway_entries['frontend_url'].get(),
                            self.gateway_entries['vpc_connection_id'].get(),
                            self.gateway_entries['info_title'].get(),
                            self.gateway_entries['info_description'].get(),
                            self.gateway_entries['info_version'].get(),
                            self.gateway_entries['servers_url'].get(),
                            self.gateway_entries['base_path_default'].get()
                        )

            elif option_index == 6:  # Merge YAML Files
                # Prompt user to select the new_api YAML file
                new_api_file = filedialog.askopenfilename(
                    filetypes=[("YAML files", "*.yaml"), ("YML files", "*.yml")]
                )
                if not new_api_file:
                    return

                # Load the remote_api and new_api files
                remote_api = load_yaml(file_path)
                new_api = load_yaml(new_api_file)

                # Merge the YAML files
                merged_yaml = merge_yaml(remote_api, new_api)

                # Prompt user to save the merged YAML file
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".yml",
                    filetypes=[("YAML files", "*.yml")]
                )
                if output_file:
                    save_yaml(merged_yaml, output_file)

            # Update progress and show success message
            self.progress_var.set(100)
            messagebox.showinfo("Success", "Conversion completed successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.progress_var.set(0)

    def _convert_json_to_yaml(self, json_file, yaml_file):
        with open(json_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON file")

        with open(yaml_file, 'w') as f:
            yaml.dump(data, f, sort_keys=False)

    def _convert_yaml_to_json(self, yaml_file, json_file):
        with open(yaml_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError:
                raise ValueError("Invalid YAML file")

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2, sort_keys=False)


def main():
    import ttkbootstrap as ttk
    root = ttk.Window(themename="flatly")
    app = SwaggerConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
