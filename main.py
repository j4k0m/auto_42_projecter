#!/usr/bin/python3
import argparse, sys, PyPDF2, os, shutil

# Argument settings
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, help="Path of the PDF file.", required=True)
args = parser.parse_args(args=None if sys.argv[1::] else ['--help'])

if args.f:
    try:
        pdfReader = PyPDF2.PdfFileReader(open(args.f, 'rb'))
    except FileNotFoundError:
        print("File not found, set a valid file path.")
    else:
        project_name = pdfReader.getPage(0).extractText().split('\n')[1]
        print("Creating structure for {} project..".format(project_name))
        try:
            os.mkdir(project_name)
        except FileExistsError:
            shutil.rmtree(project_name)
            os.mkdir(project_name)
        finally:
            for i in range(1, pdfReader.numPages):
                pageText = pdfReader.getPage(i).extractText();
                if "Turn-indirectory" in pageText:
                    folderName = pageText.split("\n")[5] + pageText.split("\n")[6]
                    print(f"Folder: {folderName} Created.")
                    os.mkdir(f"{project_name}/{folderName}")
                    fileName = pageText.split("\n")[9]
                    open(f"{project_name}/{folderName}/{fileName}", 'a').close()
                    print(f" -> File Created {fileName}.")