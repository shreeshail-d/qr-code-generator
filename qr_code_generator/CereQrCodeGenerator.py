import os
from datetime import datetime
from urllib.parse import urlparse

import segno
from PIL import Image
from new_dtect_logging.logger import DtectLogging

if __name__ == "__main__":
    # when debugging
    log_file_name = __file__.split(os.sep)[-2] + "_" + __file__.split(os.sep)[-1].split(".")[0]
    lobj_log = DtectLogging(log_file_name)
else:
    # used in parent module
    lobj_log = DtectLogging()


class CereQrCodeGenerator:
    def __init__(self,
                 pstr_error_correction: str,
                 pint_scale: int,
                 pint_border: int,
                 pint_dpi: int,
                 pstr_logo_path: str = None):
        """
        Initializes the QR Code Generator with customization options.
        :param pstr_error_correction: Error correction level (L, M, Q, or H).
        :param pint_scale: Pixel size of each QR code module.
        :param pint_border: Thickness of the QR code's border.
        :param pint_dpi: Dots per inch (DPI) for the output image.
        :param pstr_logo_path: Path to the logo image (optional).
        """
        try:
            # Validate input types for the constructor
            if not isinstance(pstr_error_correction, str):
                raise TypeError("pstr_error_correction must be a string")
            if not isinstance(pint_scale, int):
                raise TypeError("pint_scale must be an integer")
            if not isinstance(pint_border, int):
                raise TypeError("pint_border must be an integer")
            if not isinstance(pint_dpi, int):
                raise TypeError("pint_dpi must be an integer")
            if pstr_logo_path is not None and not isinstance(pstr_logo_path, str):
                raise TypeError("pstr_logo_path must be a string or None")

            # Assigning parameters after validation
            self.lstr_error_correction = pstr_error_correction.upper()  # Error correction level
            self.lint_scale = pint_scale
            self.lint_border = pint_border
            self.lint_dpi = pint_dpi
            self.lstr_logo_path = pstr_logo_path
            lobj_log.logger.info(f"QR Code Generator initialized with error correction {self.lstr_error_correction}, "
                                 f"scale {self.lint_scale}, border {self.lint_border}, dpi {self.lint_dpi}")
        except TypeError as e:
            lobj_log.logger.error(f"Type error: {str(e)}", exc_info=True)
            raise  # Re-raise the error for higher-level handling if needed

    def generate_qr_code(self,
                         pstr_base_url: str,
                         pstr_vector_format: bool = False,
                         pstr_foreground_color: str = 'black',
                         pstr_background_color: str = 'white',
                         pstr_result_dir: str = './output_qr_codes',
                         pfl_relative_logo_size: float = 0.2,
                         pint_relative_logo_position: int = 2) -> str:
        """
        Generates a QR code, handling vector/raster formats and optional logo embedding.
        :param pstr_base_url: The URL or text to encode in the QR code.
        :param pstr_vector_format: A boolean element created to know if the final result sbe saved in vector format(i.e. svg) or not
        :param pstr_foreground_color: QR code module color.
        :param pstr_background_color: QR code background color.
        :param pstr_result_dir: Directory to save the generated QR code.
        :param pint_relative_logo_position: Defines the position of the logo inside the QR code.
        :param pfl_relative_logo_size: Defines the size of logo with respect to QR code.
        :return: Path to the generated QR code file.
        """

        try:
            # Validate input types for the generate_qr_code method
            if not isinstance(pstr_base_url, str):
                raise TypeError("pstr_base_url must be a string")
            if not isinstance(pstr_vector_format, bool):
                raise TypeError("pstr_vector_format must be a boolean")
            if not isinstance(pstr_foreground_color, str):
                raise TypeError("pstr_foreground_color must be a string")
            if not isinstance(pstr_background_color, str):
                raise TypeError("pstr_background_color must be a string")
            if not isinstance(pstr_result_dir, str):
                raise TypeError("pstr_result_dir must be a string")
            if not isinstance(pfl_relative_logo_size, float):
                raise TypeError("pstr_result_dir must be a float")
            if not isinstance(pint_relative_logo_position, int):
                raise TypeError("pstr_result_dir must be a int")

            # Debug logging: print input parameters
            lobj_log.logger.debug(
                f"Generating QR code for URL: {pstr_base_url}, with error correction: {self.lstr_error_correction}, "
                f"foreground color: {pstr_foreground_color}, background color: {pstr_background_color}, "
                f"vector format: {pstr_vector_format}")

            # Adjust error correction level for Micro QR Codes
            lstr_error_correction = self.lstr_error_correction

            # Generate QR code with adjusted error correction
            lobj_qr = segno.make(
                pstr_base_url,
                error=lstr_error_correction
            )

            if not os.path.exists(pstr_result_dir):
                os.makedirs(pstr_result_dir)
                lobj_log.logger.info(f"Created output directory: {pstr_result_dir}")
            else:
                lobj_log.logger.debug(f"Output directory already exists: {pstr_result_dir}")

            lstr_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            lstr_url_name = urlparse(pstr_base_url).netloc.replace('.', '_')

            try:
                if self.lstr_logo_path:
                    # Case 1: Logo needed, vector format required
                    if pstr_vector_format:
                        raise Exception("SVG format is not allowed when embedding a logo.")
                    # Case 2: Logo needed, no vector format
                    else:
                        # Initially use PNG format for processing
                        lstr_qr_file_name = f"qr_code_{lstr_url_name}_{lstr_timestamp}.png"
                        lstr_qr_path = os.path.join(pstr_result_dir, lstr_qr_file_name)
                        lobj_qr.save(lstr_qr_path, scale=self.lint_scale, border=self.lint_border, dpi=self.lint_dpi,
                                     dark=pstr_foreground_color, light=pstr_background_color)

                        self._embed_logo_in_png(lstr_qr_path, self.lstr_logo_path, pint_relative_logo_position,
                                                pfl_relative_logo_size)
                        return lstr_qr_path

                else:
                    # Case 3: No logo, vector format required
                    if pstr_vector_format:
                        lstr_svg_path = os.path.join(pstr_result_dir, f"qr_code_{lstr_url_name}_{lstr_timestamp}.svg")
                        lobj_qr.save(lstr_svg_path, scale=self.lint_scale, border=self.lint_border,
                                     dark=pstr_foreground_color, light=pstr_background_color, kind='svg')
                        return lstr_svg_path

                    # Case 4: No logo, no vector format
                    else:
                        lstr_qr_path = os.path.join(pstr_result_dir, f"qr_code_{lstr_url_name}_{lstr_timestamp}.png")
                        lobj_qr.save(lstr_qr_path, scale=self.lint_scale, border=self.lint_border, dpi=self.lint_dpi,
                                     dark=pstr_foreground_color, light=pstr_background_color)
                        return lstr_qr_path

            except FileNotFoundError as e:
                lobj_log.logger.error(f"File path issue: {str(e)}", exc_info=True)
                raise
            except ValueError as e:
                lobj_log.logger.error(f"Invalid parameter value: {str(e)}", exc_info=True)
                raise

        except Exception as e:
            lobj_log.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def _embed_logo_in_png(pstr_qr_path: str, pstr_logo_path: str, pint_relative_logo_position: int,
                           pfl_relative_logo_size: float):
        """
        Embed a logo into a PNG QR code.
        :param pstr_qr_path: Path to the QR code PNG file.
        :param pstr_logo_path: Path to the logo image.
        :param pint_relative_logo_position: Defines the position of the logo inside the QR code.
        :param pfl_relative_logo_size: Defines the size of logo with respect to QR code.
        """

        try:
            lobj_qr_image = Image.open(pstr_qr_path)
            lobj_logo = Image.open(pstr_logo_path)

            lint_qr_width, lint_qr_height = lobj_qr_image.size
            lint_logo_size = int(min(lint_qr_width, lint_qr_height) * pfl_relative_logo_size)
            lobj_logo = lobj_logo.resize((lint_logo_size, lint_logo_size), Image.Resampling.LANCZOS)

            lint_position = ((lint_qr_width - lint_logo_size) // pint_relative_logo_position,
                             (lint_qr_height - lint_logo_size) // pint_relative_logo_position)
            lobj_qr_image.paste(lobj_logo, lint_position, lobj_logo if lobj_logo.mode == "RGBA" else None)
            lobj_qr_image.save(pstr_qr_path)
            lobj_log.logger.info(f"Logo embedded in PNG QR code and saved to: {pstr_qr_path}")
        except Exception as e:
            lobj_log.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise

# # Debug Example usage
# if __name__ == "__main__":
#     lobj_cere_qr_code = CereQrCodeGenerator(pstr_error_correction='H', pint_scale=100, pint_border=4, pint_dpi=300,
#                                             pstr_logo_path='/home/cerelabs/Workarea/shreeshail/practice/cere_qr_code_generator/cere_qr_code_generator/data/cerelabs_logo.jpeg')
#
#     # Call the method with a sample URL and a logo path
#     output_path = lobj_cere_qr_code.generate_qr_code(
#         'https://www.cerelabs.com/index',
#         pstr_vector_format=True,
#         pstr_foreground_color='blue',
#         pstr_background_color='white'
#     )
#     print(output_path)
