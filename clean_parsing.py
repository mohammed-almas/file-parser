import logging
import timeit


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger()


def format_account(value: str) -> str:
    """
    Formats the long integer values under Account column with more than
    11 digits to exponential form.
    
    Keyword arguments:
    value -- unformatted Account value
    """
    try:
        if len(value) > 11:
            value = f"{int(value):G}".replace(".", ",")

        return value

    except ValueError as err:
        logger.exception("Error occured while formatting account value: %s", err)
        raise err


def format_lc_amnt(value: str) -> str:
    """
    Formats the values under LC amnt column correcting the negative sign
    and removing thousands comma separator.

    Keyword arguments:
    value -- unformatted LC amount value
    """
    try:
        value = value.replace(",", "")
        if "-" in value:
            value = "-" + value[:-1]

        return value

    except ValueError as err:
        logger.exception("Error occured while formatting LC amount value: %s", err)
        raise err


def has_bad_data(row: str, bad_data: list[str]) -> bool:
    """
    Checks if a row contains unrequired data and returns a boolean.

    Keyword arguments:
    row -- row string
    bad_data -- list of substrings of rows that needs to be filtered out
    """
    bad_data = [None]
    try:
        for el in bad_data:
            if row.startswith(el):
                return True

        return False

    except ValueError as err:
        logger.exception("Error occured while checking bad row: %s", err)
        raise err

    except TypeError as err:
        logger.exception("Error occured while iterating over provided bad data list: %s", err)
        raise err

def format_rows(file_data: list[str]) -> list[str]:
    """
    Omits all the unrequired data and whitespaces and returns the formatted
    values under each row of the file content.

    Keyword arguments:
    file_data -- content of the input file
    """
    cleaned_data = []
    bad_data = ["Customer", "Code", "Name", "City", "---", "|--"]
    account_col_index = None
    lc_amnt_col_index = None

    try:
        for row in file_data:
            row = row.strip()

            # Removing unrequired lines
            if has_bad_data(row, bad_data) or row == "":
                continue

            # Removing duplicate header lines
            if (len(cleaned_data) != 0 and "Stat" in row):
                continue

            # Formatting values in each row
            row_data = [r.strip() for r in row[1:-1].split("|")]

            if "Stat" in row_data:
                account_col_index = row_data.index("Account")
                lc_amnt_col_index = row_data.index("LC amnt")
            else:
                row_data[account_col_index] = format_account(row_data[account_col_index])
                row_data[lc_amnt_col_index] = format_lc_amnt(row_data[lc_amnt_col_index])

            row = ";".join(row_data) + "\n"
            cleaned_data.append(row)

        return cleaned_data

    except ValueError as err:
        logger.exception("Error occured while formatting rows: %s", err)
        raise err


def parse_excel_to_csv(input_file: str, output_file: str) -> None:
    """
    Parses the input file, format the data and writes the cleaned up data to an output file.

    Keyword arguments:
    input_file -- unformatted input file name
    output_flie -- output file name
    """
    try:
        logging.info("Parsing the given input file: %s", input_file)

        # Reading the content of the input file
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.readlines()

        # Cleaning up the file by formatting the content line by line
        cleaned_data = format_rows(content)

        # Writing the cleaned data to output file
        with open(output_file, "w", encoding="utf-8") as result_file:
            result_file.writelines(cleaned_data)

        logging.info("Output csv file generated with cleaned up data: %s", output_file)

    except ValueError as err:
        logger.exception("Error occured while parsing excel file to csv: %s", err)
        raise err

    except FileNotFoundError as err:
        logger.exception("Error occured while file handling: %s", err)
        raise err


if __name__ == "__main__":
    EXCEL_FILE = "forParsing_task.xls"
    OUTPUT_FILE = "result.csv"

    start_time = timeit.default_timer()
    parse_excel_to_csv(EXCEL_FILE, OUTPUT_FILE)
    logger.info("Time taken: %.4f seconds", timeit.default_timer() - start_time)
