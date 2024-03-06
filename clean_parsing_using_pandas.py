import logging
import timeit
import pandas


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
        logger.exception("Error occured with value while formatting account value: %s", err)
        raise err

    except TypeError as err:
        logger.exception("Error occured with value type while formatting account value: %s", err)
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
        logger.exception("Error occured with value while formatting LC amount value: %s", err)
        raise err

    except TypeError as err:
        logger.exception("Error occured with value type while formatting LC amount value: %s", err)
        raise err


def format_rows(data_list: list[str]) -> list[list[str]]:
    """
    Omits all the unrequired data and whitespaces and returns the formatted
    values under each row of the file content.

    Keyword arguments:
    data_list -- list of data from content of the input file
    """

    cleaned_data = []
    account_col_index = None
    lc_amnt_col_index = None

    try:
        for row in data_list:
            # Removing unrequired and duplicate header rows
            if len(row) <= 3 or (len(cleaned_data) != 0 and "Stat" in row[1]):
                continue

            # Formatting values in each row
            row_data = [value.strip() for value in row[1:-1]]

            if "Stat" in row_data:
                account_col_index = row_data.index("Account")
                lc_amnt_col_index = row_data.index("LC amnt")
            else:
                row_data[account_col_index] = format_account(row_data[account_col_index])
                row_data[lc_amnt_col_index] = format_lc_amnt(row_data[lc_amnt_col_index])

            cleaned_data.append(row_data)

        return cleaned_data

    except ValueError as err:
        logger.exception("Error occured with value while formatting rows: %s", err)
        raise err

    except TypeError as err:
        logger.exception("Error occured with value type while formatting rows: %s", err)
        raise err


def parse_excel_to_csv(input_file: str, output_file: str) -> None:
    """
    Parses the input file, formats the data and writes the cleaned up data to an output csv file.

    Keyword arguments:
    input_file -- unformatted input file
    output_flie -- output csv file
    """

    try:
        logging.info("Parsing the given input file: %s", input_file)

        # Reading the content of the input file
        content_df = pandas.read_csv(input_file, delimiter="~", names=["data"])
        data_list = content_df["data"].str.split("|")

        # Cleaning up the file by formatting the content line by line
        cleaned_data = format_rows(data_list)
        column_names = cleaned_data[0]

        # Creating a dataframe with the cleaned up data along with header
        df = pandas.DataFrame(cleaned_data[1:], columns=column_names)

        # Writing the dataframe data to csv file
        df.to_csv(output_file, header=True, index=False, sep=";")

        logging.info("Output csv file generated with cleaned up data: %s", output_file)

    except ValueError as err:
        logger.exception("Error occured with value while parsing excel file to csv: %s", err)
        raise err

    except TypeError as err:
        logger.exception("Error occured with value type while parsing excel file to csv: %s", err)
        raise err

    except FileNotFoundError as err:
        logger.exception("Error occured while file handling: %s", err)
        raise err


if __name__ == "__main__":
    EXCEL_FILE = "forParsing_task.xls"
    OUTPUT_FILE = "result_using_pandas.csv"

    start_time = timeit.default_timer()
    parse_excel_to_csv(EXCEL_FILE, OUTPUT_FILE)
    logger.info("Time taken: %.4f seconds", timeit.default_timer() - start_time)
