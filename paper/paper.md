---
title: 'LBR-Stack: ROS 2 and Python Integration of KUKA FRI for Med and IIWA Robots'
tags:
  - C++
  - Python
  - ROS 2
  - KUKA LBR Med
  - KUKA LBR IIWA
  - Hard Real-time
header-includes:
  - \usepackage{pifont}
  - \newcommand{\cmark}{\ding{51}}
  - \newcommand{\xmark}{\ding{55}}
authors:
  - name: Martin Huber
    orcid: 0000-0003-4603-6773
    corresponding: true
    affiliation: 1
  - name: Christopher E. Mower
    orcid: 0000-0002-3929-9391
    affiliation: 1
  - name: Sebastien Ourselin
    orcid: 0000-0002-5694-5340
    affiliation: 1
  - name: Tom Vercauteren
    orcid: 0000-0003-1794-0456
    equal-contrib: true
    affiliation: 1
  - name: Christos Bergeles
    orcid: 0000-0002-9152-3194
    equal-contrib: true
    affiliation: 1
affiliations:
 - name: School of Biomedical Engineering and Image Sciences, King's College London, United Kingdom
   index: 1
date: 12 May 2023
bibliography: paper.bib
---

# Summary
The `LBR-Stack` is a collection of packages that simplify the usage and extend the capabilities of KUKA's Fast Robot Interface (FRI) [@fri]. It is designed for mission critical hard real-time applications. Supported are the `KUKA LBR Med7/14` and `KUKA LBR iiwa7/14` robots in the Gazebo simulation [@gazebo] and for communication with real hardware. A demo video can be found [here](https://www.linkedin.com/posts/mhubii_robotics-opensource-ros2-activity-7009974676017848320-S3U5/?utm_source=share&utm_medium=member_desktop).

At the `LBR-Stack`'s core are two packages:

- **fri**: Integration of KUKA's original FRI client library into CMake.
- **fri_vendor**: Vendor library that integrates the **fri** into the ROS 2 build sytem.

All other packages are built on top. These include Python bindings and packages for integration into the Robot Operating System (ROS) and ROS 2:

 - **pyFRIClient**: Python bindings for the **fri**.
 - **lbr_fri_ros2_stack**: ROS 1/2 integration of the `KUKA LBR`s through the **fri_vendor**.

For brevity, and due to the architectural advantages over ROS [@ros2], only ROS 2 is considered in the following. The **lbr_fri_ros2_stack** comprises the following packages:

- **lbr_bringup**: Python library for launching the different components.
- **lbr_description**: Description files for the `Med7/14` and `iiwa7/14` robots.
- **lbr_demos**: Demonstrations for simulation and the real robots.
- **lbr_fri_msgs**: Interface Definition Language (IDL) equivalent of FRI protocol buffers.
- **lbr_fri_ros2**: FRI ROS 2 interface through `realtime_tools` [@ros_control].
- **lbr_hardware_interface**: Interface for `ros2_control` [@ros2_control].
- **lbr_moveit_config**: MoveIt 2 configurations [@moveit].

# Statement of need
<!-- statement of need in a research context -->

An overview of existing work that interfaces the KUKA LBRs from an external computer is given in Table 1. We broadly classify these works into custom communication solutions [@iiwa_stack; @kuka_sunrise_toolbox; @libiiwa] and communication solutions through KUKA's FRI UDP channel [@iiwa_ros; @iiwa_ros2]. The former can offer greater flexibility while the latter offer a well defined interface and direct software support from KUKA. Contrary to the custom communication solutions, the FRI solutions additionally enable hard real-time communication, that is beneficial for mission critical development. Stemming from translational medical research, this work therefore focuses on the FRI.

Limitations with the current FRI solutions are:

1. Only support `iiwa7/14` robots, not `Med7/14`.
2. Don't provide Python bindings.
3. Maintainability:
    * Modified client source code [iiwa_ros](https://github.com/epfl-lasa/iiwa_ros).
    * FRI client library tangled into source code [iiwa_ros2](https://github.com/ICube-Robotics/iiwa_ros2).
4. Partial support of FRI functionality. Both, [iiwa_ros](https://github.com/epfl-lasa/iiwa_ros) and [iiwa_ros2](https://github.com/ICube-Robotics/iiwa_ros2), exclusively aim at providing implementations of the ROS 1/2 hardware abstraction layer. This does not support:
    * FRI's cartesian impedance control mode.
    * FRI's cartesian control mode (FRI version 2 and above).

The first original contribution of this work is to add support for the `KUKA LBR Med7/14` robots, which, to the best author's knowledge, does not exist in any other work. The second novel contribution of this work is to provide Python bindings. This work solves the maintainability by outsourcing the FRI into the separate **fri** and **fri_vendor** packages, which leaves the FRI's source code untouched and simply provides build support. 4. is solved by defining an IDL message to KUKA's `nanopb` command and state protocol buffers in **lbr_fri_msgs**. These messages can then be interfaced from ROS 1/2 topics or from the ROS 1/2 hardware abstraction layer.

| Framework       | iiwa | Med | ROS | ROS 2  | RT | FRI | Pos | Imp | Cart Imp | HW IF  | 
| --------------- | ---- |---- | --- | ------ | -- | ---- | --- | --- | -------- | ------ |
|[lbr_fri_ros2_stack](https://github.com/kCL-BMEIS/lbr_fri_ros2_stack) | \bullet | \bullet | \bullet | \bullet | \bullet | \bullet | \bullet | \bullet | \bullet | \bullet |
| [iiwa_ros](https://github.com/epfl-lasa/iiwa_ros)                    | \bullet |         | \bullet |         | \bullet | \bullet | \bullet | \bullet |         | \bullet |
| [iiwa_ros2](https://github.com/ICube-Robotics/iiwa_ros2)             | \bullet |         |         | \bullet | \bullet | \bullet | \bullet | \bullet |         | \bullet |
| [iiwa-stack](https://github.com/IFL-CAMP/iiwa_stack)                 | \bullet |         | \bullet |         |         |         | \bullet | \bullet | \bullet |         |
| [libiiwa](https://github.com/Toni-SM/libiiwa)                        | \bullet |         | \bullet | \bullet |         |         | \bullet | \bullet | \bullet |         |
| [KST-KUKA](https://github.com/Modi1987/KST-Kuka-Sunrise-Toolbox)     | \bullet |         |         |         |         |         | \bullet | \bullet | \bullet |         |

Table: Overview of existing frameworks for interfacing the KUKA LBRs. A square indicates support for the respective feature. List of abbreviations: Hard Real-time (**RT**), Position Control (**Pos**), Impedance Control (**Imp**), Cartesian Impedance Control (**Cart Imp**), Hardware Interface (**HW IF**). 

# Acknowledgement
We want to acknowledge the work in [@iiwa_stack], as their MoveIt configurations were utilized in a first iteration of this project.

This work was supported by core funding from the Wellcome/EPSRC [WT203148/Z/16/Z; NS/A000049/1]. This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 101016985 (FAROS project).

# References
<!-- compiled paper.bib through pandoc -->
