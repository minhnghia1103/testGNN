# ccpg imports
from ccpg.cpg.cpg_api import cpg4multifiles as cpg4multifiles_ccpg
from ccpg.cpg.cpg_api import extract_funcs as extract_funcs_ccpg
from ccpg.util.helper import load_inter_results as load_inter_results_ccpg
from ccpg.util.helper import store_inter_results as store_inter_results_ccpg
from ccpg.util.cpg_statistics import print_cpg_statistics as print_cpg_statistics_ccpg
from ccpg.encoding.batch_encoding import batch_encoding as batch_encoding_ccpg

# javacpg imports
from javacpg.cpg.cpg_api import cpg4multifiles as cpg4multifiles_javacpg
from javacpg.cpg.cpg_api import extract_funcs as extract_funcs_javacpg
from javacpg.util.helper import load_inter_results as load_inter_results_javacpg
from javacpg.util.helper import store_inter_results as store_inter_results_javacpg
from javacpg.util.cpg_statistics import print_cpg_statistics as print_cpg_statistics_javacpg
from javacpg.encoding.batch_encoding import batch_encoding as batch_encoding_javacpg

from utils.setting import init_setting, logger

import time
import os


def ccpg_main(args):
    """ Main function for ccpg """
    if args.load_iresult:
        func_list, func_dict = load_inter_results_ccpg(args.iresult_path)
    else:
        func_list = extract_funcs_ccpg(args.src_path)
        func_dict = cpg4multifiles_ccpg(func_list)
    if args.store_iresult:
        store_inter_results_ccpg(args.iresult_path, func_list, func_dict)
    
    if args.encoding:    
        batch_encoding_ccpg(args.clone_classification, args.encode_path, func_list, func_dict)

    if args.statistics:
        print_cpg_statistics_ccpg(func_dict)

def javacpg_main(args):
    """ Main function for javacpg """
    if args.load_iresult:
        func_list, func_dict = load_inter_results_javacpg(args.iresult_path)
    else:
        func_list = extract_funcs_javacpg(args.src_path)
        func_dict = cpg4multifiles_javacpg(func_list)
    if args.store_iresult:
        store_inter_results_javacpg(args.iresult_path, func_list, func_dict)
    
    if args.encoding:    
        batch_encoding_javacpg(args.encode_path, func_list, func_dict)
        
        # Handle different label types based on task
        if hasattr(args, 'task') and args.task == 'code_smell':
            # Copy code smell labels for code smell detection task
            code_smell_labels_path = '../cpgnn/code_smell_labels.csv'
            if os.path.exists(code_smell_labels_path):
                logger.info(f'Copying code smell labels from {code_smell_labels_path} to {args.encode_path}')
                if os.name == 'nt':  # Windows
                    os.system(f'copy "{code_smell_labels_path}" "{args.encode_path}"')
                else:  # Unix/Linux
                    os.system(f'cp "{code_smell_labels_path}" "{args.encode_path}"')
            else:
                logger.warning(f'Code smell labels not found at {code_smell_labels_path}')
                logger.warning('Please run: python cpgnn/prepare_code_smell_data.py --input_folder <your_data_path>')
        else:
            # Default: copy clone labels for clone detection task
            clone_labels_path = '../datasets/bigclonebench/clone_labels.txt'
            if os.path.exists(clone_labels_path):
                logger.info(f'Copying clone labels from {clone_labels_path} to {args.encode_path}')
                if os.name == 'nt':  # Windows
                    os.system(f'copy "{clone_labels_path}" "{args.encode_path}"')
                else:  # Unix/Linux
                    os.system(f'cp "{clone_labels_path}" "{args.encode_path}"')
            else:
                logger.error('Clone labels not found! Please check the path: ../datasets/bigclonebench/clone_labels.txt')
                if not (hasattr(args, 'task') and args.task == 'code_smell'):
                    exit(1)
    
    if args.statistics:
        print_cpg_statistics_javacpg(func_dict)

if __name__ == '__main__':
    args = init_setting()

    strat_time = time.time()
    if args.lang == 'c':
        ccpg_main(args)
    elif args.lang == 'java':
        javacpg_main(args)
    else:
        logger.error('Unknown language: {}'.format(args.lang))
        exit(1)
    end_time = time.time()
    logger.info('Total time: {:.2f}s'.format(end_time - strat_time))