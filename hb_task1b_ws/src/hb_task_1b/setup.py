from setuptools import find_packages, setup
from glob import glob
import os
package_name = 'hb_task_1b'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name),glob('launch/*.launch.py')),
        (os.path.join('share', package_name , 'urdf'),glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'meshes'),glob('meshes/*')),
        (os.path.join('share', package_name, 'scripts'),glob('scripts/*')),
        (os.path.join('share', package_name, 'worlds'),glob('worlds/*')),


    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='akshar',
    maintainer_email='akshar@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "controller = hb_task_1b.controller:main",
            "gazebo.launch.py = hb_task_1b.gazebo.launch:main",
            "service_node = hb_task_1b.service_node:main",
            "hb_task1b.launch.py = hb_task_1b.launch:main",
            

        ],
    },
)
