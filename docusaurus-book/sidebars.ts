import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'doc',
      id: 'index',
      label: 'Home',
    },
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'introduction/what-is-physical-ai',
        'introduction/evolution-of-systems',
        'introduction/why-this-matters',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Foundations',
      items: [
        'foundations/ai-robotics-connection',
        'foundations/hardware-overview',
        'foundations/software-overview',
      ],
      collapsed: true,
    },
    {
      type: 'category',
      label: 'How to Learn',
      items: [
        'approach/hands-on-philosophy',
        'approach/prerequisites',
        'approach/how-to-use-this-book',
      ],
      collapsed: true,
    },
    {
      type: 'category',
      label: 'Real-World Applications',
      items: [
        'applications/use-cases',
      ],
      collapsed: true,
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module1/index',
        'module1/chapter-1-middleware',
        'module1/chapter-2-ros2-basics',
        'module1/chapter-3-rclpy-bridge',
        'module1/chapter-4-urdf',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module2/introduction',
        'module2/chapter-1-physics-environment',
        'module2/chapter-2-gazebo-physics',
        'module2/chapter-3-unity-interaction',
        'module2/chapter-4-sensor-simulation',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Ethics & Future',
      items: [
        'ethics/responsible-ai',
        'ethics/future-directions',
      ],
      collapsed: true,
    },
    {
      type: 'doc',
      id: 'glossary',
      label: 'Glossary',
    },
    {
      type: 'doc',
      id: 'writing-guidelines',
      label: 'Writing Guidelines (Internal)',
    },
  ],
};

export default sidebars;
