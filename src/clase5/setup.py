from setuptools import find_packages, setup

package_name = 'clase5'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/counter_demo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='javier',
    maintainer_email='javier@example.com',
    description='ROS 2 Jazzy counter demo package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'counter_publisher = clase5.counter_publisher:main',
            'counter_subscriber = clase5.counter_subscriber:main',
        ],
    },
)
