import pandas as pd
import glob

# Find all right leg CSV files
csv_files = glob.glob('0010*R_Leg.csv', recursive=True)

for file_path in csv_files:
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Print first few rows before permutation
    print(f"\nProcessing: {file_path}")
    print("\nBefore permutation:")
    print(df[['T', 'H1', 'H2']].head(3))
    
    # Store original column values
    df_t = df['T'].copy()
    df_h1 = df['H1'].copy()
    df_h2 = df['H2'].copy()
    
    # Permute columns
    df['T'] = df_h2
    df['H1'] = df_t
    df['H2'] = df_h1
    
    # Print first few rows after permutation
    print("\nAfter permutation:")
    print(df[['T', 'H1', 'H2']].head(3))
    
    # Verify the permutation
    print("\nVerification:")
    print(f"Original T is now in H1: {all(df_t == df['H1'])}")
    print(f"Original H1 is now in H2: {all(df_h1 == df['H2'])}")
    print(f"Original H2 is now in T: {all(df_h2 == df['T'])}")
    
    # Save only if verification passes
    if all([
        all(df_t == df['H1']),
        all(df_h1 == df['H2']),
        all(df_h2 == df['T'])
    ]):
        df.to_csv(file_path, index=False)
        print("\nVerification passed - File saved successfully")
    else:
        print("\nWARNING: Verification failed - File not saved")
    
    print("-" * 50)

print(f"\nCompleted processing {len(csv_files)} files")