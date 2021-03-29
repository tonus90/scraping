# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['vacancy2803']


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            ready_salary = self._get_salary_hh(item['salary'])
            item['min_salary'] = ready_salary[0]
            item['max_salary'] = ready_salary[1]
            item['val'] = ready_salary[2]
        elif spider.name == 'sjru':
            ready_salary = self._get_salary_sj(item['salary'])
            item['min_salary'] = ready_salary[0]
            item['max_salary'] = ready_salary[1]
            item['val'] = ready_salary[2]
        collection = self.db[spider.name]
        collection.insert_one(item)
        del item['salary']
        return item

    def _get_salary_hh(self, sal):
        try:
            my_list = []
            for i in sal:
                if i[0].isdigit():
                    my_list.append(i.replace(u'\xa0', ''))
                else:
                    my_list.append(i.replace(' ', ''))
            print(my_list[0])
            print(my_list[1])
            if len(my_list)==7:
                min_s = float(f'{my_list[1]}')
                max_s = float(f'{my_list[3]}')
                val = sal[5]
            elif my_list[0] == 'от' and len(my_list) < 6:
                min_s = float(f'{my_list[1]}')
                max_s = None
                val = sal[3]
            elif my_list[0] == 'до' and len(my_list) < 6:
                min_s = None
                max_s = float(f'{my_list[1]}')
                val = sal[3]
            else:
                min_s = None
                max_s = None
                val = None
            return (min_s, max_s, val)
        except Exception as err:
            print(err)
            min_s = None
            max_s = None
            val = None
            return (min_s, max_s, val)

    def _get_salary_sj(self, sal):#получим зп
        val = None
        el = []
        my_list = []
        my_list1 = []
        if sal[0].isalpha():
            for j in sal:
                my_list.append(j.replace(u'\xa0', ' '))
            for i in my_list.pop().split(' '):
                if i.isdigit():
                    el.append(i)
                else:
                    val = i
            my_list.append(''.join(el))
            my_list.append(val)
        for i in sal:
            my_list1.append(i.replace(u'\xa0', ''))
        if my_list1[0].isdigit():
            for i in sal:
                my_list.append(i.replace(u'\xa0', ''))

        try:
            if my_list[0].isdigit() and len(my_list)==4:
                min_s = float(f'{my_list[0]}')
                max_s = float(f'{my_list[1]}')
                val = my_list[3]
            elif my_list[0].isdigit() and len(my_list)==3:
                min_s = float(f'{my_list[0]}')
                max_s = None
                val = my_list[2]
            elif my_list[0] == 'от':
                min_s = float(f'{my_list[2]}')
                max_s = None
                val = my_list[3]
            elif my_list[0] == 'до':
                min_s = None
                max_s = float(f'{my_list[2]}')
                val = my_list[3]
            else:
                min_s = None
                max_s = None
                val = None
            return (min_s, max_s, val)
        except IndexError as err:
            print(err)
            return (None, None, None)


