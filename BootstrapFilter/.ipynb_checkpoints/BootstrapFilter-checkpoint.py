"""测试哈，这个是帮助文档哦


"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


class BootstrapFilter1:
    def run1(self):
        """执行run脚本
        
        Args:
            class(int): ab
            type(float): abc
            
        Returns:
            啥也不返回
            
        Notes:
            你也是个人才哈
        """
        # Sample from the initial distribution
        self.x[0, :] = np.ravel(self.initial_sampler())
        for t in range(1, self.t_max):
            # Go forward in time in the hidden Markov chain using transition probability
            self.x[t, ] = self.transition(self.x[t-1, ], t)
            # Compute importance weights using likelihood function
            weights = self.likelihood(y_t=self.y[t, ], x_t=self.x[t, ])
            weights = weights / np.sum(weights)
            # Resample the particles according to the weights
            resampled_indexes = np.random.choice(np.arange(self.n), size=self.n, replace=True, p=weights)
            self.x = self.x[:, resampled_indexes]


class BootstrapFilter:
    """Base class implementing a BootstrapFilter (see Sequential Monte Carlo in Practice - A. Doucet, page 11)."""
    def __init__(self, p_x0, transition, likelihood, n, y):
        # Store values into fields and functions into methods
        self._initial_sampler = p_x0
        self._transition = transition
        self._likelihood = likelihood
        self.n = n
        self.y = y
        self.t_max = np.size(self.y, 0)
        self.x = np.zeros((self.t_max, self.n))

    def initial_sampler(self):
        """
        Method used to sample particles at time t=0 of the algorithm.

        Returns
        ----------
        Samples from p(x_0).
        :rtype: np.array
        """
        return self._initial_sampler(n=self.n)

    def transition(self, x, t):
        """
        Method implementing the transition probability p(x_t | x_{t-1}). Set by the constructor __init__().

        :param x: Current value of the hidden Markov chain, denoted x_{t-1}. Will be used to sample x_t.
        :type x: np.array
        :return: A sample x_t from p(x_t | x_{t-1}).
        :rtype: np.array
        """
        return self._transition(x, t)

    def likelihood(self, y_t, x_t):
        """
        Likelihood function p(y_t | x_t). This is used to compute the weights.

        :param y_t: Observed value y at time t, for which we want to evaluate the likelihood.
        :type y_t: np.array
        :return: New weight p(y_t | x_t).
        :rtype: np.array
        """
        return self._likelihood(y_t=y_t, x_t=x_t)

    def run(self):
        """执行run脚本
        
        :return: 啥也不返回
        :rtype: None
        """
        # Sample from the initial distribution
        self.x[0, :] = np.ravel(self.initial_sampler())
        for t in range(1, self.t_max):
            # Go forward in time in the hidden Markov chain using transition probability
            self.x[t, ] = self.transition(self.x[t-1, ], t)
            # Compute importance weights using likelihood function
            weights = self.likelihood(y_t=self.y[t, ], x_t=self.x[t, ])
            weights = weights / np.sum(weights)
            # Resample the particles according to the weights
            resampled_indexes = np.random.choice(np.arange(self.n), size=self.n, replace=True, p=weights)
            self.x = self.x[:, resampled_indexes]

    def __repr__(self):
        """Representation of the class. This is can be used together with eval() to know everything there is to know
        about a specific instance of this class. Overriding a non-so-helpful default."""
        return "BootstrapFilter(p_x0={}, transition={}, likelihood={}, n={}, y={})".format(
            self._initial_sampler, self._transition, self._likelihood, self.n, self.y
        )

    def __str__(self):
        """Pretty print function for reporting."""
        return "Object of Class BootstrapFilter implementing a basic SMC algorithm."


class BootstrapFilter2:
    """Base class implementing a BootstrapFilter (see Sequential Monte Carlo in Practice - A. Doucet, page 11)."""
    def __init__(self, p_x0, transition, likelihood, n, y):
        """Constructor of BootstrapFilter. It takes the marginal prior probability :math:`p(x_0)`, the transition
        probability :math:`p(x_t | x_{t-1})` and the likelihood density function :math:`p(y_t | x_t)`. Notice that since
        this SMC algorithm is a BootstrapFilter weights are found by evaluating the likelihood.

        Parameters
        ----------
        p_x0 : function
               Marginal prior probability :math:`p(x_0)` used to sample the initial hidden states.
        transition : function
                     Transition probability used by the hidden Markov chain to move forward in time.
        likelihood : function
                     Likelihood function given :math:`x_t` (since y are conditionally independent).
        n : int
            Number of particles. This is the number of samples used at each step.
        y : ndarray
            Observed data. This is generated further down in the script.

        Attributes
        ----------
        tmax : int
               Size of y. Used to determine how many time steps to run (:math:`t_{\\text{max}} + 1`).
        x : ndarray
            Numpy array of size (:math:`t_{\\text{max}}+1`, :math:`1`).

        notes
        ----------
        本部分介绍如何在Python文件的注释中使用reStructuredText来表示数学公式，如下为文本外

        .. math:: p(x_t \mid x_{t-1})  \quad p(y_t \mid x_t) \quad p(x_0)

        同时，也可以在文本中表示，比如 :math:`p(x_0)`或者 :math:`p(x_t \mid x_{t-1})`

        Examples
        --------
        Here we show the example introduced by Gordon (1993) [1]_. First, we define the initial distribution, the
        transition and the likelihood function/emission.

        >>> import numpy as np
        >>> from numpy.random import normal
        >>> from scipy import stats
        >>> import matplotlib.pyplot as plt
        >>> initial_sampler = lambda n: normal(loc=0.0, scale=np.sqrt(10), size=(n, 1))
        >>> transition = lambda x, t: normal(loc=(0.5*x + 25*(x / (1 + x**2)) + 8*np.cos(1.2*t)), scale=np.sqrt(10))
        >>> likelihood = lambda y_t, x_t: stats.norm.pdf(x=y_t, loc=(x_t**2/20), scale=1.0)
        >>> emission = lambda x_t: normal(loc=(x_t**2/20), scale=1.0)

        Next, we construct a dataset with :math:`t_{\\text{max}}` data points (excluding :math:`x_0`).

        >>> t_max = 100                       # Maximum time t up to which we generate data
        >>> n = 100                           # Number of particles
        >>> dim = 1                           # Number of dimensions. For illustrative purposes will be 1
        >>> x = np.zeros((t_max+1, dim))      # Container for x hidden values
        >>> y = np.zeros((t_max+1, dim))      # Container for y observed values
        >>> x[0, :] = initial_sampler(n=1)    # Sample x_0 from the initial distribution
        >>> y[0, :] = np.nan                  # Set y_0 to be NA since observed process starts at y_1

        Alternate between transition and emission sampling

        >>> for t in range(1, t_max+1):
        ... x[t, :] = transition(x[t-1, :], t)  # Sample x_t from the transition distribution p(x_t | x_{t-1})
        ... y[t, :] = emission(x[t, :])         # Sample y_t given x_t from the emission distribution p(y_t | x_t)

        Finally, instantiate and run the model.

        >>> model = BootstrapFilter(p_x0=initial_sampler, transition=transition, likelihood=likelihood, n=n, y=y)
        >>> model.run()

        We can see from the result that it is indeed working.

        >>> means = np.mean(model.x, axis=1)
        >>> fig, ax = plt.subplots()
        >>> ax.plot(np.arange(101), means)
        >>> ax.plot(np.arange(101), x)
        >>> plt.show()

        References
        ----------
        .. [1] Gordon, N.J., Salmond, D.J. and Smith, A.F.M.. "Novel approach to nonlinear/non-Gaussian Bayesian state
           estimation." IEEE Proceedings F, Radar and Signal Processing 140 , no. 2 (1993): 107-113.


        """
        # Store values into fields and functions into methods
        self._initial_sampler = p_x0
        self._transition = transition
        self._likelihood = likelihood
        self.n = n
        self.y = y
        self.t_max = np.size(self.y, 0)
        self.x = np.zeros((self.t_max, self.n))

    def initial_sampler(self):
        """
        Method used to sample particles at time t=0 of the algorithm.

        Returns
        ----------
        Samples from p(x_0).
        :rtype: np.array
        """
        return self._initial_sampler(n=self.n)

    def transition(self, x, t):
        """
        Method implementing the transition probability p(x_t | x_{t-1}). Set by the constructor __init__().

        :param x: Current value of the hidden Markov chain, denoted x_{t-1}. Will be used to sample x_t.
        :type x: np.array
        :return: A sample x_t from p(x_t | x_{t-1}).
        :rtype: np.array
        """
        return self._transition(x, t)

    def likelihood(self, y_t, x_t):
        """
        Likelihood function p(y_t | x_t). This is used to compute the weights.

        :param y_t: Observed value y at time t, for which we want to evaluate the likelihood.
        :type y_t: np.array
        :return: New weight p(y_t | x_t).
        :rtype: np.array
        """
        return self._likelihood(y_t=y_t, x_t=x_t)

    def run(self):
        """
        执行run脚本
        :return: 啥也不返回
        :rtype: None
        """
        # Sample from the initial distribution
        self.x[0, :] = np.ravel(self.initial_sampler())
        for t in range(1, self.t_max):
            # Go forward in time in the hidden Markov chain using transition probability
            self.x[t, ] = self.transition(self.x[t-1, ], t)
            # Compute importance weights using likelihood function
            weights = self.likelihood(y_t=self.y[t, ], x_t=self.x[t, ])
            weights = weights / np.sum(weights)
            # Resample the particles according to the weights
            resampled_indexes = np.random.choice(np.arange(self.n), size=self.n, replace=True, p=weights)
            self.x = self.x[:, resampled_indexes]

    def __repr__(self):
        """Representation of the class. This is can be used together with eval() to know everything there is to know
        about a specific instance of this class. Overriding a non-so-helpful default."""
        return "BootstrapFilter(p_x0={}, transition={}, likelihood={}, n={}, y={})".format(
            self._initial_sampler, self._transition, self._likelihood, self.n, self.y
        )

    def __str__(self):
        """Pretty print function for reporting."""
        return "Object of Class BootstrapFilter implementing a basic SMC algorithm."
