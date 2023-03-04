import os
from pathlib import Path
from threading import Thread
from fs import open_fs
from fs.walk import Walker
import sys
from lib.Database import Database
from time import sleep



excluding_list = []
temp_list = []
pattern1 = ['т','┤','Х','и','╨','д','Б', ' ']
pattern2 = ['_DE', '_MA', '_GE', '_SO', '_EN', '_BI']


class Correcture(Thread):
    def __init__(self) -> None:
        super(Correcture, self).__init__()
        
        self.search = Database().select('Search')
        self.filter = Database().select('Filter')
        self.exclude = Database().select('ExcludeDirs')
        self.ierrors = Database().select('IgnoreErrors')

        
    def run(self) -> None:
        """        try:
            self.sync()
        except Exception as e:
            print("Error by syncronization with database: %s" % e)"""
        updated_list = list(self.walk_for_files())      
        updated_list = list(dict.fromkeys(updated_list))

        for u in updated_list:
            for p in pattern1:
                if p in u:
                    temp_list.append(u)
 
        updated_list = list(dict.fromkeys(temp_list))
        
        final_list = ([s.replace('т',
                            '').replace('┤',
                                        '').replace('и',
                                                    '').replace('╨',
                                                                '').replace('д',
                                                                            '').replace('Б',
                                                                                        '').replace('Х',
                                                                                                    '').replace(' ',
                                                                                                                '').replace('Д',
                                                                                                                            '') for s in updated_list])
        for (old, new) in zip(updated_list, final_list):
            print(os.rename(old, new))
            
        print(final_list)
        
        

        
        
                    

        

    def sync(self) -> None:
        print("Loading database...")
        if self.search.isalnum():
            print(f"Search Method: {self.search}")
        else:
            print("Something goes wrong by loading the database search entry...")
        sleep(2)
        if self.filter is not None:
            print(f"Filter Settings: {self.filter}")
        else:
            print("Something goes wrong by loading the database filter entrys...")
        sleep(2)
        if self.exclude is not None:
            print(f"Exclude Settings: {self.exclude}")
        else:
            print("Something goes wrong by loading the database exclude entrys...")
        sleep(2)
        if self.ierrors == 0:
            print("Ignore Errors: True")
        elif self.ierrors == 1:
            print("Ignore Errors: False")
        else:
            print("Something goes wrong by loading the database ignore errors entry...")

        
    def walk_for_files(self) -> list:
        start = str(Path.home())
        start = open_fs(start)
        walker = Walker(filter=self.filter, 
                       search=self.search, 
                       exclude_dirs=self.exclude, 
                       ignore_errors=self.ierrors)

        for path in walker.files(start):
            i = str(Path(start.getsyspath(path)))
            i = excluding_list.append(i)
        
        return excluding_list
            
    def old_list(self) -> list:
        return list(self.walk_for_files())


if __name__ == "__main__":
    try:
        thread = Correcture()
        thread.start()
        thread.join()
    except KeyboardInterrupt:
        sys.exit("\nClosed...")
