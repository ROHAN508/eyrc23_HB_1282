from setuptools import find_packages, setup

package_name = 'hb_task5a'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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

        ],
    },
)
