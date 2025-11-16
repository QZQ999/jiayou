# This Python file uses the following encoding: utf-8
"""
    Windows版本启动脚本 - 无需C++编译器
    Author: Fu Qingxu,CASIA (Modified for Windows)

    使用方法:
        python main_windows.py --cfg your_config.jsonc
"""
import os, atexit, platform

def SET_NUM_THREADS(internal_threads):
    os.environ['NUM_THREADS'] = str(internal_threads)
    os.environ['OPENBLAS_NUM_THREADS'] = str(internal_threads)
    os.environ['MKL_NUM_THREADS'] = str(internal_threads)
    os.environ['OMP_NUM_THREADS'] = str(internal_threads)
SET_NUM_THREADS(1)

# do NOT edit this func
def pytorch_gpu_init(cfg):
    import torch
    from UTIL.auto_gpu import sel_gpu
    torch.set_num_threads(int(os.environ['NUM_THREADS']))
    seed = cfg.seed; device = cfg.device
    torch.manual_seed(seed)
    torch.set_printoptions(precision=4, sci_mode=False)
    # e.g. device='cpu'
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    if not 'cuda' in device: return
    if device == 'cuda':
        gpu_index = sel_gpu().auto_choice()
    else: # e.g. device='cuda:0'
        gpu_index = int(device.split(':')[-1]) if ',' not in device else device.split(':')[-1]
        # parse gpu_party, e.g. cuda-1#2
        if cfg.gpu_party.startswith('#'):
            cfg.gpu_party = f"{cfg.device.replace(':', '-')}{cfg.gpu_party}"
        cfg.manual_gpu_ctl = True
        if cfg.gpu_fraction!=1: torch.cuda.set_per_process_memory_fraction(cfg.gpu_fraction, gpu_index)
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_index)
    cfg.device = 'cuda' if ',' not in device else device # remove ':x', the selected gpu is cuda:0 from now on
    torch.cuda.manual_seed(seed)
    if cfg.use_float64:
        torch.set_default_dtype(torch.float64)


def register_daemon(cfg):
    from UTIL.hmp_daemon import start_periodic_daemon
    start_periodic_daemon(cfg)


if __name__ == '__main__':
    import numpy

    # ====== Windows专用: 跳过Cython编译 ======
    print("Windows平台检测: 使用Python进程池 (不需要C++编译器)")

    from UTIL.colorful import *
    from UTIL.config_args import prepare_args
    from UTIL.win_pool import SmartPool  # 使用Windows版本的进程池

    cfg = prepare_args()
    register_daemon(cfg)

    # Set numpy seed
    numpy.random.seed(cfg.seed)
    numpy.set_printoptions(3, suppress=True)

    # Get mem-sharing process pool (Windows版本)
    print亮绿(f"初始化Windows进程池: {cfg.num_threads} 个并行环境")
    assert cfg.num_threads % cfg.fold == 0, ('Use n process to run n*m parallel threads!')
    smart_pool = SmartPool(fold=cfg.fold, proc_num=cfg.num_threads // cfg.fold, base_seed=cfg.seed)
    atexit.register(smart_pool.party_over)  # failsafe, handles pool cleanup

    # Pytorch has to be init AFTER the process pool starts, set pytorch seed
    pytorch_gpu_init(cfg=cfg)

    # Prepare everything else
    from task_runner import Runner
    runner = Runner(process_pool=smart_pool)

    # GO! GO! GO!
    print亮绿('=' * 70)
    print亮绿('开始训练!')
    print亮绿('=' * 70)
    runner.run()
    runner.conclude_experiment()

    # DONE!
    print绿('--- All jobs finished ---')
    smart_pool.party_over()

elif platform.system()!="Linux":
    # Reload config for Windows multiprocessing
    from UTIL.config_args import prepare_args
    cfg = prepare_args(vb=False)
