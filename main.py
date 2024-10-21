import bs4
import pandas as pd
import argparse

args = argparse.ArgumentParser()

args.add_argument("--input", type=str, required=True)
args.add_argument("--output", type=str, required=True)

args = args.parse_args()


def get_html_from_file(file_path):
    with open(file_path, encoding="utf8") as file:
        return file.read()


if __name__ == "__main__":

    input_file = args.input
    assert input_file.endswith(".html"), "Input file must be an HTML file"

    output_file = args.output
    assert output_file.endswith(".csv") or output_file.endswith(
        ".md"
    ), "Output file must be a CSV or MD file"

    soup = bs4.BeautifulSoup(get_html_from_file(input_file), "html.parser")

    papers = soup.find_all("tr", class_="gsc_a_tr")

    data = []

    for paper in papers:
        title = paper.find("a", class_="gsc_a_at").text
        authors = paper.find("div", class_="gs_gray").text
        year = paper.find("span", class_="gsc_a_h gsc_a_hc gs_ibl").text
        url = paper.find("a", class_="gsc_a_at").get("href")
        publication = paper.find("div", class_="gs_gray").find_next("div").text

        data.append(
            {
                "title": title,
                "authors": authors,
                "year": int(year) if year else 0,
                "url": url,
                "publication": publication,
            }
        )

    df = pd.DataFrame(data)

    df.sort_values("year", ascending=False, inplace=True)

    df = df[df["year"].astype(int) >= 2011]

    if output_file.endswith(".csv"):
        df.to_csv("papers.csv", index=False)
    else:
        with open("publications.md", "w", encoding="utf8") as file:
            for year in df["year"].unique():
                file.write(f"## {year}\n")
                for _, row in df[df["year"] == year].iterrows():
                    file.write(f"[{row['title']}]({row['url']})\n")
                    file.write(f"{row['authors']} - {row['publication']}\n\n")

    print("Done!")
