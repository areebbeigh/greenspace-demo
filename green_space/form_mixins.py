class FormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, attrs in self.style_attrs.items():
            # self.fields[field_name].widget.attrs.update({
            #     'class': 'form-control',
            #     'placeholder': self.placeholders.get(field_name, '')
            # })
            self.fields[field_name].widget.attrs.update(attrs)