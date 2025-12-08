import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from slugify import slugify
from striprtf.striprtf import rtf_to_text

# ---------------------------------------------------
# Load and combine Excel files
# ---------------------------------------------------

# %%
trump_immigration_index1 = pd.read_excel('trump_and_immigration1_1000.xlsx')
trump_immigration_index2 = pd.read_excel('trump_and_immigration1001_2000.xlsx')
trump_immigration_index3 = pd.read_excel('trump_and_immigration2001_2811.xlsx')

trump_immigration_final = pd.concat([
    trump_immigration_index1,
    trump_immigration_index2,
    trump_immigration_index3
], ignore_index=True)

# %%
print("Combined DataFrame:")
print(trump_immigration_final.head())
print("Number of rows in final index:", len(trump_immigration_final))

trump_immigration_final.to_excel('trump_and_immigration_final.xlsx', index=False)
print("Final index saved successfully!")


# ---------------------------------------------------
# Load converted text files
# ---------------------------------------------------

text_folder = "/Users/tiasiasaunders/Desktop/code/personal_code_projects/cj_final_project/file_raw_text"

files = [f for f in os.listdir(text_folder) if f.endswith(".txt")]

files_df = pd.DataFrame(files, columns=["filename"])

files_df["index"] = (
    files_df["filename"]
    .str.replace(".txt", "", regex=False)
    .apply(lambda x: slugify(x))
    .str[:25]
)

files_df = files_df.drop_duplicates(subset="index")

print("Files index:")
print(files_df.head())


# ---------------------------------------------------
# Load Excel index and clean title column
# ---------------------------------------------------

excel_df = pd.read_excel("trump_and_immigration_final.xlsx")

excel_df.columns = excel_df.columns.str.lower().str.replace(" ", "_")

excel_df["index"] = (
    excel_df["title"]
    .astype(str)
    .apply(lambda x: slugify(x))
    .str[:25]
)

excel_df = excel_df.drop_duplicates(subset="index")

print("\nExcel index:")
print(excel_df.head())


# ---------------------------------------------------
# Merge text files list with Excel metadata
# ---------------------------------------------------

final_data = pd.merge(files_df, excel_df, on="index", how="inner")

print("\nMerged final data:")
print(final_data.head())
print(f"\nNumber of matched articles: {len(final_data)}")

final_data.to_csv("final_data.csv", index=False)
print("final_data saved as final_data.csv")


# ---------------------------------------------------
# Add full file path for each article
# ---------------------------------------------------

final_data["filepath"] = text_folder + "/" + final_data["filename"]

print("\nFinal Data With Filepaths:")
print(final_data.head())


# Create an empty list to store rows
articles_list = []

# Loop through each row of final_data
for idx, row in final_data.iterrows():
    filepath = row["filepath"]
    filename = row["filename"]

    # Read all lines from the text file
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        continue

    # Append each line as a row with the filename
    for line in lines:
        # Strip newline characters
        line = line.strip()
        if line:  # skip empty lines
            articles_list.append({"filename": filename, "sentence": line})

# Create DataFrame from the list
articles_df = pd.DataFrame(articles_list)

print("Articles DataFrame head:")
print(articles_df.head())

# Join articles_df back to final_data on filename
articles_df = pd.merge(articles_df, final_data, on="filename", how="inner")

print("\nArticles DataFrame with metadata:")
print(articles_df.head())

# Optional: save to CSV
articles_df.to_csv("articles_df.csv", index=False)
print("Articles saved to articles_df.csv")

# Count unique articles
num_articles = articles_df["filename"].nunique()
print(f"Number of articles in articles_df: {num_articles}")


## starting descriiptive statistics 

print("\nSummary of final_data:")
print(final_data.describe(include="all"))

print("\nSummary of articles_df:")
print(articles_df.describe(include="all"))


# Example visualization: Distribution of articles by publication date
# Filter only CNN and Fox News
source_counts = final_data[final_data['publication.1'].isin(['CNN', 'Fox News'])]
source_counts = source_counts['publication.1'].value_counts().reset_index()
source_counts.columns = ['publication', 'count']

# Plot
plt.figure(figsize=(6,4))
sns.barplot(data=source_counts, x='publication', y='count', palette=['blue','red'])

plt.title('Number of Articles by Source')
plt.xlabel('News Source')
plt.ylabel('Number of Articles')
plt.xticks(rotation=0)
plt.figtext(0.99, 0.01, "Graphic by Tiasia Saunders 11/08/2025", horizontalalignment='right', fontsize=9)

plt.tight_layout()
plt.savefig('/Users/tiasiasaunders/Desktop/code/personal_code_projects/cj_final_project/article_counts_by_source.png')
plt.show()

