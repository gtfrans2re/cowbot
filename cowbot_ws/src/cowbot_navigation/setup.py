from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'cowbot_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*.bash')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cowbot',
    maintainer_email='francoisgonothitoure@gmail.com',
    description='Cowbot navigation and obstacle avoidance package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_interface = cowbot_navigation.robot_interface:main',
            'robot_control = cowbot_navigation.robot_control_client:main',
            'robot_control_debug = cowbot_navigation.robot_control_debug:main',
        ],
    },
)
