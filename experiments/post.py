all_tables_data = [['SI. No.', 'STUDENT NAME', 'CLASS', 'SECTION', 'AGE', 'M/F', 'PARENTS NAME', 'RE VISION', 'LE VISION', 'REMARKS'], ['1', 'ARABINA BANU', '1 8+', '', '6', 'F', 'SYED BABU', '', '', ''], ['2', 'ARBINA BANU', '-1/-', '', '6', 'F', 'YASEEN', '', '', ''], ['3', 'BIBI FATHIMA', '-JJ-', '', '6', 'F', 'SAMIULLA', '', '', ''], ['4', 'KAUSAR BANU', '-11-', '', '6', 'F', 'ILIYAS', '', '', ''], ['5', 'MOHAMMAD SHAHID', '-1)-', '', '6', 'M', 'SYED IMAM SAB', '', '', ''], ['6', 'SUHANA BANU', '-11-', '', '6', 'F', 'MUBARAK', '', '', ''], ['1', 'AYISHA', '2 st', '', '7', 'F', 'MOHAMAD ASIF', '', '', '1'], ['8', 'AZIMA BANU', '-1-', '', '7', 'F', 'YASIN', '', '', 'L'], ['9', 'MUDASIR', '-11-', '', '7', 'M', 'ISMAIL', '', '', '2'], ['10', 'NANAWALI', '-11-', '', '7', 'm', 'SHAIK IMAMSAR', '', '', '2 /'], ['1)', 'SAJAN', '-11-', '', '7', 'm', 'SADIK', '', '', ''], ['12', 'SYED RIHAN BASHA', '-1)-', '', '7', 'M', 'SYED YASIN', '', '', ''], ['13', 'TASMIYA BANU', '-11-', '', '7', 'F', 'SHAIK DADAPEER', '', '', 'L'], ['14', 'HAMEED', '3rd', '', '8', 'm', 'SHAIK KHASIM SAS', '', '', '2'], ['15', 'AFFIYA', '-11-', '', '8', 'F', 'IMAM', '', '', 'L'], ['16', 'FATHIMA ZOHRA', '-11-', '', '8', 'F', 'SHAIK IMAMSAB', '', '', 'L'], ['17', 'SYED UMER', '-11-', '', '8', 'm', 'SYED BUDEN SAB', '', '', ''], ['18', 'MUBARAK', '-11-', '', '8', 'm', 'DADADEER', '', '', ''], ['19', 'THABREJ', '-11-', '', '8', 'm', 'SYED DATEL', '', '', 'L'], ['20', 'ALIYA BANU', '-11-', '', '8', 'F', 'ILIYAS', '', '', ''], ['21', 'ASIF REZA', '3rd', '', '8', 'm', 'DEER MOHAMMAD', '', '', ''], ['22', 'ZOYA FAROOQI', '-11-', '', '8', 'F', 'SYED UMAR FAROOQ', '', '', ''], ['23', 'AFFRIN BANU', '4th', '', '9', 'F', 'SYED YASEEN', '', '', ''], ['24', 'ILAHEEN BANU', '-11-', '', '9', 'F', 'SÃO\nSYED YASEEN', '', '', ''], ['25', 'NIGAR FATHIMA', '-11-', '', '9', '', 'MUBARAK', '', '', ''], ['26', 'SHAIK SOHAIL', '-11-', '', '9', 'F', 'SHEK DADADEER', '', '', ''], ['27', 'SOHAIL', '-1-', '', '9', 'm', 'VASEEN', '', '', '2'], ['28', 'RAHEELA BANU', '', '', '10', '', 'SYED KHASIM', '', '', '2'], ['29', 'SOHAIL', '-11-', '', '10', 'm', 'SYED PATEL', '', '', '/'], ['30', 'SANIYA', '-11-', '', '10', 'F', 'DADADEER', '', '', '- Absent-'], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '', '']]

def docType(table):
    if (table[0] == ['SI. No.', 'STUDENT NAME', 'CLASS', 'SECTION', 'AGE', 'M/F', 'PARENTS NAME', 'RE VISION', 'LE VISION', 'REMARKS']): 
        return 1
    elif (table[0] == ['Sl. No.', 'STUDENT NAME', 'CLASS', 'SECTION', 'AGE', 'M/F', 'PARENTS NAME', 'RE VISION', 'LE VISION', 'REMARKS']):
        return 1
    elif (table[0] == ['Sl. No.', 'STUDENT NAME', 'CLASS / SEC.', 'DOB', 'M/F', 'PARENTS NAME', 'MOBILE NUMBER', 'RIGHT EYE', '', '', '', 'LEFT EYE', '', '', '', 'SATS ID', 'REMARKS']):
        return 2
    elif (table[0] == ['SI. No.', 'STUDENT NAME', 'CLASS / SEC.', 'DOB', 'M/F', 'PARENTS NAME', 'MOBILE NUMBER', 'RIGHT EYE', '', '', '', 'LEFT EYE', '', '', '', 'SATS ID', 'REMARKS']):
        return 2
    else:
        return 0
    
print(docType(all_tables_data))

def sanitizeSLNO(table):
    if len(table) < 2:  # If table has less than 2 rows, no need to sanitize
        return table
    
    for i in range(1, len(table)):  # Start from the second row (index 1)
        table[i][0] = str(i)  # Set the first column to the row index (as a string)
    
    return table

def removeEmptyRows(table):
    if len(table) < 2:  # If table has less than 2 rows, no need to process
        return table
    
    # Keep the header (first row) and filter the rest
    return [table[0]] + [row for row in table[1:] if row[1].strip() != ""]

def sanitizeClass(table):
    if len(table) < 2:  # If table has less than 2 rows, no need to sanitize
        return table
    
    for i in range(1, len(table)):  # Start from the second row (index 1)
        if len(table[i]) > 2 and table[i][2].startswith('-') and table[i][2].endswith('-'):
            if len(table[i-1]) > 2:
                table[i][2] = table[i-1][2]
    
    return table


print(sanitizeClass(all_tables_data))
