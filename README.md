# qr-code-generator
A PYTHON PROJECT THAT GENERATE S QR CODE
# Cere QR Code Generator

The **Cere QR Code Generator** is a Python-based utility for generating customizable QR codes. It supports embedding
logos, adjusting error correction levels, and saving QR codes in raster (PNG) or vector (SVG) formats.

## Example usage

```python
from cere_qr_code_generator.CereQrCodeGenerator import CereQrCodeGenerator

lobj_cere_qr_code = CereQrCodeGenerator(pstr_error_correction='H', pint_scale=100, pint_border=4, pint_dpi=300)

# Call the method with a sample URL and a logo path
output_path = lobj_cere_qr_code.generate_qr_code(
    'https://www.cerelabs.com/index',
    pstr_vector_format=True,
    pstr_foreground_color='red',
    pstr_background_color='white'
)
print(output_path)
```

## Change log

### v1.0.0

```text
- Generate QR codes with customizable error correction levels (L, M, Q, H).
- Support for raster (PNG) and vector (SVG) formats.
- Embed logos into QR codes.
- Adjust colors, scale, border size, and DPI.
- Handles exceptions with detailed logging.
```
