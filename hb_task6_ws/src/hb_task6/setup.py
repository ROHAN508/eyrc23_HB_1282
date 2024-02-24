from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'hb_task6'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'scripts'), glob('scripts/*'))
    
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='premsai',
    maintainer_email='premsai78801@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'feedback = hb_task6.feedback:main',
        'controller = hb_task6.controller:main',
        'controllerik = hb_task6.controller_ik:main',
        'nextgoal = hb_task6.nextGoalPub:main',
        'map = hb_task6.mapping:main',
        'interp = hb_task6.interpolation:main',
        'controllerik2 = hb_task6.controller_ik2:main',
        'map2 = hb_task6.mapping2:main',
        'interp2 = hb_task6.interpolation2:main',
        'controllerik3 = hb_task6.controller_ik3:main',
        'map3 = hb_task6.mapping3:main',
        'interp3 = hb_task6.interpolation3:main',
        'StopFlag = hb_task6.stop_bot_srv:main',
        'server = hb_task6.StopFlagServer:main',
        'img = hb_task6.nextGOal1:main'
        ],
    },
)
