
import subprocess
import os
import sys


# Function to get the list of modified files in the commit
def get_modified_files():
    try:
        # Get the list of modified files (slx files) in the current commit
        result = subprocess.run(['git', 'diff', commit1, commit2, '--name-only', '--diff-filter=M'], 
                                stdout=subprocess.PIPE, 
                                text=True,      # Ensure output is in string format
                                check=True)     # Raise an error if the command fails
        # Filter to include only Simulink model files (.slx or .mdl)
        modified_files = [line for line in result.stdout.splitlines() if (line.endswith('.slx') or line.endswith('.mdl'))]
        return modified_files
    except subprocess.CalledProcessError as e:
        print(f"Error getting modified files: {e}")
        return []

# Function to call SimDiff for each file
def run_simdiff_for_files(file):
        try:
            # Call the difftool (replace 'simdiff' with the actual command if different)
            report_file = f"{reportsDir}/" + file.removesuffix(".slx") + ".peerreview.html"
            print(f"    report_file= {report_file}")

            # Ensure report directory is created if it doesn't exist
            report_path = os.path.dirname(report_file)
            os.makedirs(report_path, exist_ok=True)
            
            path_to_diff_tool = f'"\'C:/Program Files/EnSoft/SimDiff Automation/sd4.exe\' -l $LOCAL -r $REMOTE -export {report_file}"' 
            config_cmd = f'git config --local difftool.sd4.cmd {path_to_diff_tool}'
            #print(f"    config_cmd= {config_cmd}")
            subprocess.run(config_cmd, text=True, check=True, shell=True)
 
            diff_cmd = f'git difftool -y -t sd4 {commit1} {commit2} {file}'
            #print(f"    diff_cmd= {diff_cmd}")
            subprocess.run(diff_cmd, text=True, shell=True)
            
            #print(f"    SimDiff ran successfully for {file}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error running SimDiff on {file}: {e}")

def main():
    modified_files = get_modified_files()
    if modified_files:
        print("Modified Simulink models:")
        for file in modified_files:
            print(f" - {file}")
            run_simdiff_for_files(file)
    else:
        print("No modified Simulink models found.")

if __name__ == '__main__':
    reportsDir = sys.argv[1]
    commit1 = sys.argv[2]
    commit2 = sys.argv[3]
    main()
