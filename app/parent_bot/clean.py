input_file_path = 'book.txt'
output_file_path = 'book2.txt'

with open(input_file_path, 'rb') as input_file:
    # Read the content of the file as bytes
    content = input_file.read()

    try:
        # Attempt to decode the content as UTF-8
        decoded_content = content.decode('utf-8')
    except UnicodeDecodeError as e:
        # Handle the decoding error by removing problematic bytes
        decoded_content = content.decode('utf-8', errors='ignore')
        print(f"Decoding error: {e}")

# Write the modified content back to the file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(decoded_content)

print(f"Modified content written to {output_file_path}")
