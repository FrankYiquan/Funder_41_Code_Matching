# Funder Matching for ScholarWorks Internal 41 Code

This repository is used to matching **external funders**—as identified in OpenAlex metadata associated with scholarly articles—to their corresponding **41 codes** or **internal Funders** used in ScholarWorks. This process serves as a **preprocessing step** for downstream tasks such as linking academic articles to their respective grants in ScholarWorks.

## 🔍 Background

Two key platforms(both have API) are integral to this matching process:

### 1. [OpenAlex](https://openalex.org/)
OpenAlex is an open-access bibliographic catalog of scientific articles, authors, institutions, and funders. It provides structured metadata about scholarly outputs, including:
- Article-level details
- Associated funders and, often, grants
- Unique OpenAlex IDs for each funder (e.g., `https://openalex.org/F123456789`)

> **Note:** Each funder listed in OpenAlex includes an OpenAlex ID that can be used to retrieve structured metadata about the funder.

### 2. [Research Organization Registry (ROR)](https://ror.org/)
ROR provides open, persistent identifiers for research organizations, and includes:
- Organization metadata
- Alternative names
- Parent-child organizational structures

> **Note:** While OpenAlex sometimes provides ROR IDs for funders, this linkage is not always consistent or complete.

## 🧩 Matching Process

The matching pipeline consists of two main steps:

### Step 1: Extract Unique Funders from Articles
- Parse metadata of academic articles (sourced from OpenAlex) associated with a specific funder.
- Restrict results to a self-defined time interval (e.g., past 5 years).
- Collect a list of **unique funders** and their **OpenAlex IDs**.

### Step 2: Match Funders to Internal 41 Codes
- Use the OpenAlex and (optionally) ROR metadata to enrich funder names.
- Normalize names and aliases to identify matching entries in the Internet 41 code registry used by ScholarWorks.
- Output a mapping file linking each OpenAlex funder to its respective Internet 41 code.

## ✅ Example Output

An example of output csv file would look something like this:


| unique_funder             | matched_funder                                           | matched_funder_code                              | matched_object |
|---------------------------|----------------------------------------------------------|--------------------------------------------------|----------------|
| National Science Foundation | National Science Foundation (United States, Alexandria) - NSF | 41___NATIONAL_SCIENCE_FOUNDATION_(ALEXANDRIA) | child/Exact    |



## 📁 Project Structure
```text
Funder_41_Code_Matching/
├── internal_funders/           # Normalized internal funder reference provided by Scholarworks
├── resources/                  # Stored supporting csv file (e.g. country code, internal funder 41 code)
├── unique_funders/             # Extracted unique funder lists from OpenAlex (step 1)
├── edge_cases.py                 # Handles special or ambiguous funder matching logic
├── environment.yml             # Conda environment definition file
├── funder_match.py             # Core matching logic between OpenAlex funders and Internet 41 codes
├── main.py                     # Main script to run the pipeline end-to-end (step 2)
├── new_match_output.csv        # Output CSV with matched funders and codes
└── README.md                   # Project documentation (you’re here!)
```

## 🚀 Getting Started

To run this repository, follow these steps to set up the virtual environment and run the code.

### 1️⃣ Set up the Conda Virtual Environment

Open your terminal in the project root directory and run:

```bash
# Create a new Conda environment with all the required dependencies
conda env create -f environment.yml

# Activate the newly created environment
conda activate funder41Code_env
```

### 2️⃣ Extract Unique Funders and Their OpenAlex IDs

To extract all **unique funders** and their associated **OpenAlex funder IDs** from articles, run the following function in:

📄 `funder41Code/unique_funders/unique_funder_and_count.py`

#### 🔧 How to Use

Call the function `get_all_funder(start_year: int, end_year: int, schoolId: str)` with:

- `start_year`, `end_year`: the time interval for articles to be pulled from OpenAlex
- `schoolId`: the OpenAlex institution ID (you can find this by searching the institution on [OpenAlex](https://openalex.org))

#### 🧪 Example Code

To extract funders for **Brandeis University** (OpenAlex ID: `I6902469`) from 2018 to 2024:

```python
schoolId = "I6902469"  # OpenAlex ID for Brandeis University
get_all_funder(2018, 2024, schoolId)
```

This will collect and save a list of unique funders acknowledged in articles affiliated with the institution, along with their OpenAlex funder IDs, for the given time range.

#### ✅  Example Output

The output of the code above is stored in:

```
unique_funders/output/sorted_funder_data.csv
```

It would look something like this:

| funder_name             | count                                           | openalex_id                      
|---------------------------|----------------------------------------------------------|--------------------------------------------------|
| National Science Foundation | 606 | F4320306076 |

Each row represents a unique funder extracted from OpenAlex-matched articles, including:

- **funder_name**: the display name of the funder  
- **count**: how many times this funder appears across the matched articles  
- **openalex_id**: the unique OpenAlex ID for this funder

The repository uses this CSV file for further analysis, reporting, or fuzzy matching in downstream tasks.

> **Note:** This method can run range from 10 - 20 minutes depend on the volume of articles are inculded in the time interval.

### 3️⃣ Run Matching Script (`main.py`)

Run the main matching script to perform fuzzy matching between the unique funders and the 41-code funder reference list.

```bash
python main.py
```
This executes the `main()` method, which performs the following steps:

---

#### 🔁 Matching Process

For each funder in `unique_funders/output/sorted_funder_data.csv`:

1. **Extract Metadata**
   - Use the funder's OpenAlex ID to call OpenAlex API and retrieve:
     - Alternative funder names (from OpenAlex)
     - Country code (if available)
     - ROR ID (if available)
   - If a **ROR ID** is available:
     - Call the ROR API to fetch:
       - More alternative names (aliases, labels)
       - Parent ROR ID (if the funder is a sub-unit)

2. **Fuzzy Match Against Internal 41 Code List**
   - Loop through all internal funders from:
     ```
     internal_funders/output/new_internal_41.csv
     ```
   - For each record, perform fuzzy string matching using all available names for the external funder.

3. **Matching Rules**
   The logic for determining a match is as follows:

   - ✅ **Direct Match(Exact)**
     - `fuzzy_score >= 95` **and** `country_code matches` → **Match found**

   - 🧪 **Edge Case(EdgeCase)**
     - If no match is found, this may be:
       - A European or Chinese grant where the named funder is not the overseeing funder

   - 🏛 **Parent Institution Match**
     - If a **parent ROR ID** is available:
       - Fetch parent institution info
       - Retry the 3 matching conditions above using the parent’s metadata

   - 💡 **Fallback Suggestion(HighestScore)**
     - If still no match and no parent ror Id:
       - Suggest the internal funder with the **highest similarity score**, which is >= 60
       - Mark this as a **non-confident suggestion** for **manual validation**




    The "confidence level" of the matching rules: Exact = EdgeCase > HighestScore


---

#### 🗂 Output

The final matching results are saved to:

```
final_match_output.csv
```

With the following columns:

```
unique_funder,matched_funder,matched_funder_code,matched_object
```

Where:
- `unique_funder`: Funder name from OpenAlex
- `matched_funder`: Best-matched name from internal 41 list
- `matched_funder_code`: Associated code from internal list
- `matched_object`: includes a tag that summarizes how the match was made.  

> `matched_object` Format: `child|parent/MatchType`  
> There are **four possible `MatchType` values**:
>
> - `Exact`: Direct fuzzy match with country (score ≥ 95)
> - `EdgeCase`: Fuzzy match without country OR a known ambiguous funder situation (e.g. EU or China)
> - `HighestScore`: No match found, fallback suggestion based on highest fuzzy score
> - `not_found`: No match or valid suggestion, even after using parent ROR
>
> And the prefix:
> - `child`: The match was based on the original funder's data  
> - `parent`: The match was based on the parent institution's data (via ROR)

#### 🔍 Examples

| `matched_object`     | Meaning                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `child/Exact`        | Funder matched using its own metadata with a direct (Exact) match       |
| `parent/EdgeCase`    | Funder matched using its parent’s metadata, under an edge-case fallback |
| `child/HighestScore` | No official match found, but suggests best guess using fuzzy score only |
| `child/not_found`    | No match found, and no usable parent ROR ID available 
| `...`    | ...

This structure allows downstream systems and reviewers to easily assess the match quality and determine whether manual verification is needed.

#### ✅ Example Final Output
| unique_funder             | matched_funder                                           | matched_funder_code          |            matched_object|           
|---------------------------|----------------------------------------------------------|--------------------------------------------------| --------------------------------------------------|
| National Science Foundation | "National Science Foundation (United States, Alexandria) - NSF" | 41___NATIONAL_SCIENCE_FOUNDATION_(ALEXANDRIA) |child/Exact |

## 📁 Additional File: `internal_funders/`

This folder preprocessed and normalized internal funder data:

### 🧩 Purpose

The internal funder CSV file is **normalized** to improve fuzzy matching performance. It separates:

- `funder_name`: Cleaned and standardized name of the funder  
- `country`: Country code for location-aware matching  
- `city`: Optional city data to help resolve duplicates  
- `ascyloym`: Shortened aliases or acronyms used by the funder (if applicable)

These internal records represent the **full set of accepted funders** in the system and do not change over time.

> ✅ **Note:** There is no need to re-run this processing step. This list is fixed and included as part of the system configuration.

---

### 🛠 `oneFunderMatch.py` (Optional)

This script allows you to test the fuzzy matching logic on **a single, user-defined funder** rather than processing the full external list.

- Mainly intended for **debugging or development**
- You can safely **ignore this file** if you're only running the standard full-matching pipeline
