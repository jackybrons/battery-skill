# Safety, thermal runaway, fast charging, and control

## Safety tasks

Distinguish fault detection, fault diagnosis, early warning, root-cause inference, and thermal-runaway propagation. Do not call a post-event classifier an early-warning model.

Signals may include voltage, current, temperature, gas, pressure, force/swelling, acoustic/ultrasonic data, and impedance. Early-warning studies should report lead time and false alarms under defined conditions. Pack safety must distinguish cell-level thermal runaway from propagation through modules/packs.

Safety-critical deployment claims require robustness, uncertainty/failure-mode analysis, realistic sensors, and latency evidence. Laboratory abuse tests alone do not establish field reliability.

## Fast charging and control

Fast charging trades charging time against degradation, lithium-plating risk, temperature, voltage constraints, energy efficiency, and safety.

Relevant approaches include model predictive control, Bayesian optimization, active learning, reinforcement learning, surrogate models, and hybrid electrochemical/ML control.

Define the charging protocol, C-rate/current limits, SOC window, temperature, voltage constraints, and objective. For RL, state reward and safety constraints physically. For BO/active learning, state the expensive experimental objective and acquisition/selection logic.

A faster protocol is not automatically better. Report ageing/safety consequences under consistent starting conditions. Claims about lithium-plating avoidance require direct or validated indirect evidence.
