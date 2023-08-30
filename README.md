# Smart Bill Analyzer


Smart Bill Analyzer is an ongoing Data Science and Engineering project for Semester 5, designed to simplify the often tedious task of manually analyzing bills and invoices. Our goal is to help users effortlessly extract essential information from bills and invoices and provide valuable insights, enabling them to make informed financial decisions.

## Team Members

- [Malshan (malshanCS)](https://github.com/malshanCS)
- [Thilakna (200007thilakna)](https://github.com/200007thilakna)
- [Nadun (codened)](https://github.com/codened)

## Overview

Smart Bill Analyzer is currently focused on internet bills from two popular Internet Service Providers (ISPs) in Sri Lanka: SLT (Sri Lanka Telecom) and Dialog. We aim to expand our bill analysis capabilities to cover a wider range of bills and invoices in the future.

## Technologies Used

Our project leverages a range of cutting-edge technologies to deliver its functionality:

- **OpenCV**: OpenCV is used for image preprocessing, enabling us to enhance the quality of bill images before extracting text.

- **PIL (Python Imaging Library)**: PIL complements OpenCV by facilitating additional image processing tasks.

- **Pytesseract**: Pytesseract is employed for text extraction from bill images, ensuring accurate data retrieval.

- **NLTK (Natural Language Toolkit)**: NLTK aids in tokenization, enabling us to break down extracted text into meaningful units for analysis.

- **Streamlit**: Streamlit powers the web application interface, providing users with a seamless and user-friendly experience.

## How It Works

Smart Bill Analyzer simplifies the process of bill analysis in the following steps:

1. **Image Preprocessing**: When you upload a bill image, Smart Bill Analyzer uses OpenCV and PIL to clean and enhance the image, making it suitable for text extraction.

2. **Text Extraction**: Pytesseract is then applied to the preprocessed image to extract relevant text data from the bill.

3. **Tokenization**: NLTK is used to tokenize the extracted text, breaking it down into meaningful chunks.

4. **Analysis and Insights**: The tokenized data is then analyzed to provide users with valuable insights about their bill, such as total amount due, due date, and any other pertinent information.

5. **Web Application**: All of this functionality is accessible through our user-friendly web application powered by Streamlit.

## Getting Started

To get started with Smart Bill Analyzer, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/smart-bill-analyzer.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:

   ```bash
   cd app_streamliy
   streamlit run app.py
   ```

4. Upload a bill image and let Smart Bill Analyzer work its magic!

## Future Plans

We have ambitious plans for the future of Smart Bill Analyzer, including:

- Expanding bill support to cover a broader range of bill types and providers.
- Implementing advanced machine learning algorithms for more accurate analysis.
- Enhancing the user interface for an even more intuitive experience.
- Incorporating user feedback to continuously improve the application.

## Contributing

We welcome contributions from the open-source community to make Smart Bill Analyzer even better. Feel free to open issues, suggest new features, or submit pull requests. Together, we can simplify bill analysis for everyone!

## License

This project is licensed under the [MIT License](LICENSE), which means you are free to use, modify, and distribute the code for both personal and commercial purposes.

---

**Smart Bill Analyzer** is here to make your life easier by handling the complexities of bill analysis. We hope you find it useful and look forward to your feedback and contributions!
