# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import logging

from scipy.optimize import minimize

from qiskit.aqua.components.optimizers import Optimizer

logger = logging.getLogger(__name__)


class COBYLA(Optimizer):
    """Constrained Optimization By Linear Approximation algorithm.

    Uses scipy.optimize.minimize COBYLA
    See https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    """

    CONFIGURATION = {
        'name': 'COBYLA',
        'description': 'COBYLA Optimizer',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'cobyla_schema',
            'type': 'object',
            'properties': {
                'maxiter': {
                    'type': 'integer',
                    'default': 1000
                },
                'disp': {
                    'type': 'boolean',
                    'default': False
                },
                'rhobeg': {
                    'type': 'number',
                    'default': 1.0
                },
                'tol': {
                    'type': ['number', 'null'],
                    'default': None
                }
            },
            'additionalProperties': False
        },
        'support_level': {
            'gradient': Optimizer.SupportLevel.ignored,
            'bounds': Optimizer.SupportLevel.ignored,
            'initial_point': Optimizer.SupportLevel.required
        },
        'options': ['maxiter', 'disp', 'rhobeg'],
        'optimizer': ['local']
    }

    def __init__(self, maxiter=1000, disp=False, rhobeg=1.0, tol=None):
        """
        Constructor.

        For details, please refer to
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html.

        Args:
            maxiter (int): Maximum number of function evaluations.
            disp (bool): Set to True to print convergence messages.
            rhobeg (float): Reasonable initial changes to the variables.
            tol (float): Final accuracy in the optimization (not precisely guaranteed).
                         This is a lower bound on the size of the trust region.
        """
        self.validate(locals())
        super().__init__()
        for k, v in locals().items():
            if k in self._configuration['options']:
                self._options[k] = v
        self._tol = tol

    def optimize(self, num_vars, objective_function, gradient_function=None, variable_bounds=None, initial_point=None):
        super().optimize(num_vars, objective_function, gradient_function, variable_bounds, initial_point)

        res = minimize(objective_function, initial_point, tol=self._tol, method="COBYLA", options=self._options)
        return res.x, res.fun, res.nfev
