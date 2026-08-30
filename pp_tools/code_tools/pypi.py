import requests
from bs4 import BeautifulSoup


def get_package_info(package_name):
    url = f'https://pypi.org/project/{package_name}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant information from the PyPI page
        latest_version = soup.find('span', class_='release__version').text.strip()
        release_frequency = len(soup.find_all('span', class_='release__version'))
        last_commit_date = soup.find('time', class_='relative-time')['datetime']
        documentation_quality = bool(soup.find('a', class_='reference external', href='https://readthedocs.org/'))
        
        # Other metrics can be added based on the page structure
        
        return {
            'latest_version': latest_version,
            'release_frequency': release_frequency,
            'last_commit_date': last_commit_date,
            'documentation_quality': documentation_quality,
        }
    else:
        print(f"Failed to retrieve information for {package_name}")
        return None

# Example usage
package_name = 'requests'
package_info = get_package_info(package_name)

if package_info:
    print(f"Package: {package_name}")
    print(f"Latest Version: {package_info['latest_version']}")
    print(f"Release Frequency: {package_info['release_frequency']}")
    print(f"Last Commit Date: {package_info['last_commit_date']}")
    print(f"Documentation Quality: {package_info['documentation_quality']}")
