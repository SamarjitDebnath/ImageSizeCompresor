import streamlit as st
from io import BytesIO
from lib.compressor import ImageCompressor


def main():
    st.title('Image Size Compressor')
    image_file = st.file_uploader("Upload Image", type=['jpeg', 'png', 'jpg'])
    show_file = st.empty()

    if not image_file:
        show_file.info(
            'No file is uploaded, please upload a file with ".jpeg", ".png", ".jpg" extension')
        return

    if isinstance(image_file, BytesIO):
        show_file.image(image_file)
    else:
        print('Uploaded file is not a .jpeg or .png .jpg file')

    # compress the image
    image_compressor = ImageCompressor(image_file)
    image_compressor.load_image()
    image_compressor.calculate_image_size()
    image_compressor.image_data_normalize()
    compressed_image = image_compressor.k_means_compression()

    # convert PIL image to byte stream
    compressed_image_bytes = BytesIO()
    compressed_image.save(compressed_image_bytes, format='JPEG')
    compressed_image_bytes = compressed_image_bytes.getvalue()

    # download button for image download
    btn = st.download_button(
        label="Download Image",
        data=compressed_image_bytes,
        file_name="compressed_image.jpeg",
        mime="image/jpeg"
    )

    if btn:
        st.download_button.data = None


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: Something went wrong {e}')
