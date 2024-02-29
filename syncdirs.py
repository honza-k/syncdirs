import argparse
import filecmp
import os.path
import shutil
import logging
from time import sleep


PROG_NAME = 'syncdirs'
DESCRIPTION = 'Veeam Homework - directory synchronization'


class Utils:
    def forward_copy(self, source, replica):
        """
        Traverses through source directory and compares with replica directory.
        Directories found in source but not found in replica are created in replica.
        Files found in source but not found in replica are copied from source to replica.
        Files which differ are overwritten from source to replica.

        :param source: string - source directory to be synchronized
        :param replica: string - replica directory
        """
        for _ in os.listdir(source):
            src_path = os.path.join(source, _)
            replica_path = os.path.join(replica, _)

            if os.path.isdir(src_path):
                if not os.path.isdir(replica_path):
                    os.mkdir(replica_path)
                    logging.info(f'Directory {replica_path} created in replica')
                self.forward_copy(src_path, replica_path)

            elif os.path.isfile(src_path):
                if not os.path.isfile(replica_path) or not filecmp.cmp(src_path, replica_path):
                    shutil.copy2(src_path, replica_path, follow_symlinks=False)
                    logging.info(f'File {src_path} copied to {replica_path}')

            else:
                logging.warning(f'Special file {src_path} found, it stays untreated in replica')

    def backward_remove(self, source, replica):
        """
        Traverses through replica directory and compares with source directory.
        Files and directories found in replica but not found in source are deleted from replica.

        :param source: string - source directory to be synchronized
        :param replica: string - replica directory
        """
        for _ in os.listdir(replica):
            src_path = os.path.join(source, _)
            replica_path = os.path.join(replica, _)

            if os.path.isdir(replica_path):
                if not os.path.isdir(src_path):
                    if len(os.listdir(replica_path)) > 0:
                        self.backward_remove(src_path, replica_path)
                    else:
                        os.rmdir(replica_path)
                        logging.info(f'Directory {replica_path} removed from replica')
                else:
                    self.backward_remove(src_path, replica_path)

            if os.path.isfile(replica_path):
                if not os.path.isfile(src_path):
                    os.remove(replica_path)
                    logging.info(f'File {replica_path} removed from replica')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog=PROG_NAME, description=DESCRIPTION)
    parser.add_argument('-s', '--source', help='Source Directory', type=str, required=True)
    parser.add_argument('-r', '--replica', help='Replica Directory', type=str, required=True)
    parser.add_argument('-i', '--interval', help='Synchronization Interval [sec]', type=float, required=True)
    parser.add_argument('-l', '--log', help='Log File Path', type=str, default=f'/tmp/{PROG_NAME}.log')
    parser.add_argument('--log_level', help='Log Level', type=str, default='INFO')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(args.log), logging.StreamHandler()])

    print(f"""
    {PROG_NAME} is running with these arguments:
    Source Directory "{args.source}"
    Replica Directory "{args.replica}"
    Synchronization Interval {args.interval} sec
    Log File {args.log}
    *** Stop by CTRL+C ***
    """)

    try:
        while True:
            Utils().forward_copy(args.source, args.replica)
            Utils().backward_remove(args.source, args.replica)
            sleep(args.interval)
    except KeyboardInterrupt:
        print(f'{PROG_NAME} interrupted by user')
        exit(0)
