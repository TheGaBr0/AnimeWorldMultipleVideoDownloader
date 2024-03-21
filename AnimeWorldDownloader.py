import os
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, wait
from tqdm import tqdm


def divide_list(lst, x):
    if len(lst) > x:

        sublists = []
      
        num_sublists = len(lst) // x
        if len(lst) % x != 0:
            num_sublists += 1
        
       
        for i in range(num_sublists):
            sublist = lst[i*x : (i+1)*x]
            sublists.append(sublist)
        
        return sublists
    else:
        
        return [lst]

def replace_episode_number(url, min_episode_number, max_episode_number):
    
    episode_number_index = url.find('Ep_') + 2
    
    number_of_digits = 1
    i = episode_number_index + 1  # Start from the next index after the given index
    while i < len(url) and url[i].isdigit():
        number_of_digits += 1
        i += 1
    
    episode_list = []
    
    for num in range(min_episode_number, max_episode_number + 1):
        formatted_num = str(num).zfill(2)
        episode_list.append(url[:episode_number_index + 1] + formatted_num + url[episode_number_index + number_of_digits:])
    
    return episode_list

def download_video(url, output_path, position):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(output_path, 'wb') as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc=output_path, position=position, ncols=200
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def download_multiple_videos(links, output_dir, max_downloads_in_parallel):
    with ThreadPoolExecutor(max_workers=max_downloads_in_parallel) as executor:  
        futures = []
        for i, link in enumerate(links):
            file_name = os.path.basename(link)
            output_path = os.path.join(output_dir, file_name)
            futures.append(executor.submit(download_video, link, output_path, i))

        # Wait for all threads to finish
        wait(futures)
    
    
MAX_EPISODE = 1000
MAX_DOWNLOADS_IN_PARALLEL = 50
INITIAL_EPISODE = 0


if __name__ == "__main__":
    #output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloaded_episodes")
    
    if getattr(sys, 'frozen', False):
        output_directory = os.path.join(os.path.dirname(sys.executable), "downloaded_episodes")
    else:
        output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloaded_episodes")
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    while True:
        url = input("Enter the link of an episode: ")
        try:
            max_downloads_in_parallel = int(input((f"Enter the maximum number of downloads to run simultaneously (<={MAX_DOWNLOADS_IN_PARALLEL}): ")))
            initial_episode = int(input(f"Enter the starting episode number (>{INITIAL_EPISODE}): "))
            max_episodes = int(input(f"Enter the maximum number of episodes to download (<{MAX_EPISODE}): "))
            
            if max_downloads_in_parallel <=INITIAL_EPISODE or max_downloads_in_parallel >MAX_DOWNLOADS_IN_PARALLEL:
                print(f"The number of downloads to run simultaneously should be between {INITIAL_EPISODE} and {MAX_DOWNLOADS_IN_PARALLEL}")
            elif initial_episode <= INITIAL_EPISODE or max_episodes <= 0:
                print(f"The starting episode number and the maximum number of episodes must be greater than {INITIAL_EPISODE}.")
            elif max_episodes > MAX_EPISODE:
                print(f"The maximum number of episodes cannot be greater than {MAX_EPISODE}.")
            else:
                video_links = replace_episode_number(url, initial_episode, max_episodes)
                
                video_links_sanitized = divide_list(video_links, max_downloads_in_parallel)
                
                print(f"Output directory: {output_directory}")
                print(f"Processing {max_downloads_in_parallel} episodes at a time")
                
                for video_links in video_links_sanitized:
                    download_multiple_videos(video_links, output_directory, max_downloads_in_parallel)
                break
            
                print("Download completed")
        except ValueError:
            print("Error: Please make sure to enter valid numbers for the starting episode and the maximum number of episodes.")

    
 
