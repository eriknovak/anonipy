"""Shared fixtures and configuration for the test suite."""

try:
    import torch

    HAS_GPU = torch.cuda.is_available()
except ImportError:
    HAS_GPU = False
