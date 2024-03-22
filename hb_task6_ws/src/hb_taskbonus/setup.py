from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'hb_taskbonus'

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
            'feedback = hb_taskbonus.feedback:main',
            'controller1=hb_taskbonus.controller1:main',##changed
            'map1=hb_taskbonus.mapping:main',
            'interp1=hb_taskbonus.interpolation:main',
            'nextGoal1=hb_taskbonus.nextGoal_image1:main',
            'nextGoalfunc=hb_taskbonus.nextGoal_function:main',
            'imgutl=hb_taskbonus.image_utlis:main',
            'controller2=hb_taskbonus.controller2:main',##changed
            'map2=hb_taskbonus.mapping2:main',
            'interp2=hb_taskbonus.interpolation2:main',
            'controller3=hb_taskbonus.controller3:main',##changed
            'map3=hb_taskbonus.mapping3:main',
            'interp3=hb_taskbonus.interpolation3:main',
            'nextGoal2=hb_taskbonus.nextGoal_image2:main',
            'nextGoal3=hb_taskbonus.nextGoal_image3:main',
            'startpoint=hb_taskbonus.startpointflag:main',
            'StopFlag=hb_taskbonus.StopFlagServer:main'



            
        ],
    },
)
