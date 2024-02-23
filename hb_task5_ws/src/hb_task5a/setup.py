from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'hb_task5a'

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
    maintainer='akshar',
    maintainer_email='dashakshar376@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'feedback = hb_task5a.feedback:main',
            'controller = hb_task5a.controller:main',
            'controllerik = hb_task5a.controller_ik:main',
            'nextgoal = hb_task5a.nextGoalPub:main',
            'map = hb_task5a.mapping:main',
            'interp = hb_task5a.interpolation:main',
            'controllerik2 = hb_task5a.controller_ik2:main',
            'map2 = hb_task5a.mapping2:main',
            'interp2 = hb_task5a.interpolation2:main',
            'controllerik3 = hb_task5a.controller_ik3:main',
            'map3 = hb_task5a.mapping3:main',
            'interp3 = hb_task5a.interpolation3:main',
            'StopFlag = hb_task5a.stop_bot_srv:main',
            'server =hb_task5a.StopFlagServer:main',
            'img =hb_task5a.nextGOal1:main'

        ],
    },
)
