# Installing DESI jupyter kernels at NERSC

If you're a member of the DESI collaboration, please refer to the [collaboration wiki for instructions](https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC).

For NERSC users who are not part of the DESI collaboration, please follow the steps outlined below:

1. Log into perlmutter.nersc.gov and set up the DESI code environment. Switch the environment variables to the publicly accessible EDR location using the following commands:

    ```
    source /global/common/software/desi/desi_environment.sh 23.1
    module switch desitree/edr
    ```

2. Determine your shell by using the command: echo ${SHELL}.

3. Depending on your shell, select the appropriate kernel version:
    * For /bin/bash, /bin/sh, or /bin/zsh, use the "bash" kernels. For example, `desi-edr-23.1-bash`.
    * For /bin/tcsh or /bin/csh, use the "tcsh" kernels. For example, `desi-edr-23.1-tcsh`.
    
4. Copy the chosen kernel to your home directory using the following command:
    ```
    mkdir -p ~/.local/share/jupyter/kernels
    cp -R /global/common/software/desi/kernels/desi-edr-23.1-bash ~/.local/share/jupyter/kernels
    ```
    This step will install the DESI EDR 23.1 kernel. Other available kernels are `desi-22.5`, `desi-23.1` and `desi-main`,

5. Access https://jupyter.nersc.gov/hub/login and initiate a "Perlmutter" server (Note: Do not start a "Spin" server).

6. Once the server loads your home directory and kernel definitions, navigate to a new directory where you'll save your notebooks.

7. To create a new notebook, navigate through File -> New Launcher and then click on the kernel version, such as DESI EDR 23.1.


