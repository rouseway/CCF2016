#-*- coding:utf-8 -*-
#author: raosiwei
#date: 2016-11-24

import sys,re,math
import utils

import jieba.posseg

class feat():
    def __init__(self, cust_no, keywords_num, reason_num):
        self.cust_no = cust_no

        #10种业务类型的致电次数
        self.busi_type_freq = {'010':0, '003':0, '001':0, '007':0, '015':0, \
                               '005':0, '018':0, '009':0, '008':0, '006':0 }
        #通话总时长
        self.total_call_minutes = 0
        #通话次数
        self.total_call_freq = 0
        #平均通话时长（分钟）
        self.ave_call_minutes = 0

        #每个月催办督办次数
        self.monthly_oversee_freq = [0,0,0,0,0,0,0,0,0,0,0,0]

        #合同容量
        self.contract_cap = 0

        #用电客户高能耗行业分布
        self.hec_industry_dist = {'104':0, '200':0, '101':0, '103':0, '201':0,\
                                  '106':0, '202':0, 'null':0 }

        #用电客户行业分类的分布
        self.trade_dist = {'9910':0, '9920':0, '6530':0, '6510':0, '1710':0,\
                           '1810':0, 'others':0 }

        #用电客户城乡类别分布
        self.urban_rural_dist = { '01':0, '02':0, '03':0, 'null':0 }

        #用电客户用户分类分布
        self.sort_dist = { '00':0, '01':0, '02':0, '03':0, 'others':0 }
        #用电客户负荷性质分布
        self.load_attr_dist = { '1':0, '2':0, '3':0, 'null':0 }
        #用电客户状态分布
        self.status_dist = { '0':0, '2':0, '9':0, 'null':0 }

        #用户标识次数
        self.cons_id_freq = 0
        #是否执行峰谷电价
        self.ts_flag_freq = 0

        #用户是否为低保户
        self.dibaohu_flag = 0
        #用户所属低保户类型
        self.dibaohu_type = { '01':0, '02':0 }
        #低保户用户状态
        self.dibaohu_status = { '01':0, '02':0 }

        #费控用户状态标识
        self.rca_status = { '01':0, '02':0, '03':0, 'null':0 }
        #是否实时费控
        self.rca_flag = 0

        #累计延期缴费频次
        self.pay_delay_freq = 0

        #每个月应收金额
        self.monthly_rcvbl_fee = [0,0,0,0,0,0,0,0,0,0,0,0]
        #每个月实收金额
        self.monthly_rcved_fee = [0,0,0,0,0,0,0,0,0,0,0,0]
        #每个月应收违约金
        self.monthly_rcvbl_penalty = [0,0,0,0,0,0,0,0,0,0,0,0]
        #每个月实收违约金
        self.monthly_rcved_penalty = [0,0,0,0,0,0,0,0,0,0,0,0]
        #每个月总电量
        self.monthly_t_pq = [0,0,0,0,0,0,0,0,0,0,0,0]
        #每个月总电费
        self.monthly_owe_amt = [0,0,0,0,0,0,0,0,0,0,0,0]

        #电能表类别
        self.dianneng_type = {'01':0, '02':0, '03':0, '04':0, '09':0, '10':0}

        #每个月缴费次数
        self.monthly_pay_freq = [0,0,0,0,0,0,0,0,0,0,0,0]
        #每种方式缴费次数
        self.typely_pay_freq = {'020311':0, '020101':0, '020108':0, '010101':0, '020331':0, '030201':0, \
                                '020261':0, '020271':0, '010301':0, '010106':0, '010601':0 }
        #供电单位分布
        self.org_no_dist = {'33401':0, '33402':0, '33403':0, '33404':0, '33405':0, '33406':0, \
                            '33407':0, '33408':0, '33409':0, '33410':0, '33411':0, '33420':0 }

        #accept_content关键词
        self.keywords_freq = [0]*keywords_num

        #催办电费
        self.oversee_price = 0

        #催办原因
        self.reason_freq = [0]*reason_num

        #用电类别
        self.elec_type_dist = {'201':0, '200':0, '203':0, '202':0, '300':0, '301':0, '900':0, '404':0, \
                               '405':0, '000':0, '403':0, '402':0, '401':0, '400':0, '102':0, '100':0, \
                               '504':0, '503':0, '500':0, '101':0, 'null':0 }

        #月末缴费次数
        self.monthly_end_pay_freq = [0,0,0,0,0,0,0,0,0,0,0,0]


    def update_gongdan(self, gongdan, content_keywords):
        if gongdan.urban_rural_flag in self.urban_rural_dist:
            self.urban_rural_dist[gongdan.urban_rural_flag] = 1
        if gongdan.elec_type in self.elec_type_dist:
            self.elec_type_dist[gongdan.elec_type] = 1
        org_no_abs = gongdan.org_no[:5]
        if org_no_abs in self.org_no_dist:
            self.org_no_dist[org_no_abs] = 1
        busi_type = gongdan.busi_type_code
        if len(busi_type) == 3 and busi_type in self.busi_type_freq:
            self.busi_type_freq[busi_type] += 1

        for keyword in content_keywords:
            if gongdan.accept_content.find(keyword) != -1:
                self.keywords_freq[content_keywords[keyword]] += 1


    def update_kehutonghua(self, minute):
        if minute != 0:
            self.total_call_freq += 1
            self.total_call_minutes += minute


    def update_cuibanduban(self, cuibanduban, reason_keywords):
        month = cuibanduban.get_oversee_month()
        if month != -1:
            self.monthly_oversee_freq[month-1] += 1
        if cuibanduban.oversee_reason.find("电费") != -1 or cuibanduban.oversee_content.find("电费") != -1:
            self.oversee_price += 1
        segs = jieba.posseg.cut(cuibanduban.oversee_reason)
        jieba_seg_list = list(segs)
        for i in range(len(jieba_seg_list)):
            word = jieba_seg_list[i].word.encode('utf-8')
            if word in reason_keywords:
                self.reason_freq[reason_keywords[word]] += 1


    def update_yongdiankehu(self, yongdiankehu):
        self.contract_cap = yongdiankehu.contract_cap
        if yongdiankehu.hec_industry_code in self.hec_industry_dist:
            self.hec_industry_dist[yongdiankehu.hec_industry_code] = 1
        if yongdiankehu.trade_code in self.trade_dist:
            self.trade_dist[yongdiankehu.trade_code] = 1
        if yongdiankehu.cons_sort_code in self.sort_dist:
            self.sort_dist[yongdiankehu.cons_sort_code] = 1
        if yongdiankehu.load_attr_code in self.load_attr_dist:
            self.load_attr_dist[yongdiankehu.load_attr_code] = 1
        if yongdiankehu.status_code in self.status_dist:
            self.status_dist[yongdiankehu.status_code] = 1


    def update_yonghudianjia(self, yonghudianjia):
        self.cons_id_freq += 1
        if yonghudianjia.tf_flag == '1':
            self.ts_flag_freq += 1


    def update_dibaohu(self, dibaohu):
        self.dibaohu_flag = 1
        if dibaohu.cont_type in self.dibaohu_type:
            self.dibaohu_type[dibaohu.cont_type] = 1
        if dibaohu.status in self.dibaohu_status:
            self.dibaohu_status[dibaohu.status] = 1


    def update_feikongyonghu(self, feikongyonghu):
        self.rca_flag = feikongyonghu.rca_flag
        if feikongyonghu.cons_status in self.rca_status:
            self.rca_status[feikongyonghu.cons_status] = 1


    def update_shishoudianfei(self, shishoudianfei):
        month = shishoudianfei.get_charge_month()
        if month != -1:
            self.monthly_pay_freq[month-1] += 1
        if shishoudianfei.is_delay():
            self.pay_delay_freq += 1


    def update_yingshoudianfei(self, yingshoudianfei):
        month = yingshoudianfei.get_rcvbl_month()
        if month != -1:
            self.monthly_rcvbl_fee[month-1] += yingshoudianfei.rcvbl_amt
            self.monthly_rcved_fee[month-1] += yingshoudianfei.rcved_amt
            self.monthly_rcvbl_penalty[month-1] += yingshoudianfei.rcvbl_penalty
            self.monthly_rcved_penalty[month-1] += yingshoudianfei.rcved_penalty
            self.monthly_t_pq[month-1] += yingshoudianfei.t_pq
            self.monthly_owe_amt[month-1] += yingshoudianfei.owe_amt
        if yingshoudianfei.pay_code in self.typely_pay_freq:
            self.typely_pay_freq[yingshoudianfei.pay_code] = 1


    def update_yunxingdianneng(self, yunxingdianneng):
        sort_code = yunxingdianneng.sort_code
        if sort_code in self.dianneng_type:
            self.dianneng_type[sort_code] = 1


    def update_shoufeijilu(self, shoufeijilu):
        month = shoufeijilu.get_charge_month()
        if month != -1:
            self.monthly_pay_freq[month-1] += 1
            if shoufeijilu.check_charge_at_month_end():
                self.monthly_end_pay_freq[month-1] += 1


    def check_lianxuyongdian_less_10(self):
        for i in range(10):
            if self.monthly_t_pq[i] < 10 and self.monthly_t_pq[i+1] < 10 \
                and self.monthly_t_pq[i+2] < 10:
                return 1
        return 0


    def check_dianliang_wudaoyou(self):
        wu_flag = False
        for pq in self.monthly_t_pq:
            if pq < 10:
                wu_flag = True
            elif pq > 50 and wu_flag == True:
                return 1
        return 0


    def check_dianliang_youdaowu(self):
        you_flag = False
        for pq in self.monthly_t_pq:
            if pq > 50:
                you_flag = True
            elif pq < 10 and you_flag == True:
                return 1
        return 0


    def check_dianliang_increase(self):
        for i in range(11):
            if self.monthly_t_pq[i+1] > 2*self.monthly_t_pq[i]:
                return 1
        return 0


    def check_dianliang_decrease(self):
        for i in range(11):
            if self.monthly_t_pq[i+1] < self.monthly_t_pq[i]*0.5:
                return 1
        return 0


    def check_dianliang_continue_increase(self):
        for i in range(10):
            if self.monthly_t_pq[i+2] > 1.3*self.monthly_t_pq[i+1] and \
                self.monthly_t_pq[i+1] > 1.3*self.monthly_t_pq[i]:
                return 1
        return 0

    def check_dianliang_continue_decrease(self):
        for i in range(10):
             if self.monthly_t_pq[i+2] < 0.7*self.monthly_t_pq[i+1] and \
                self.monthly_t_pq[i+1] < 0.7*self.monthly_t_pq[i]:
                 return 1
        return 0



    def output_features(self, fout):

        # /*                    客服通话相关表特征                      */ 2~57

        #输出10种业务类型的致电次数
        a = self.busi_type_freq
        fout.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d," % (a['001'], a['003'], a['005'], \
                   a['006'], a['007'], a['008'], a['009'], a['010'], a['015'], a['018']))
        #输出10种业务类型的致电总数
        amt = 0
        for freq in self.busi_type_freq:
            amt += self.busi_type_freq[freq]
        fout.write("%d," % amt)


        #输出通话平均时长
        b = 0
        if self.total_call_freq > 0:
            b = round(self.total_call_minutes*1.0 / self.total_call_freq, 2)
        fout.write("%f," % b)


        #输出每月催办督办次数
        for freq in self.monthly_oversee_freq:
            fout.write("%d," % freq)

        #输出文本特征
        fout.write("%d" % self.oversee_price)
        for freq in self.keywords_freq:
            fout.write(",%d" % freq)

        ''' #不输出督办信息
        for freq in self.reason_freq:
            fout.write(",%d" % freq)
        '''


        # /*                    用电信息相关表特征                      */

        #输出用户合同容量
        fout.write(",%d," % self.contract_cap)
        #输出用户高能耗行业分布
        b = self.hec_industry_dist
        fout.write("%d,%d,%d,%d,%d,%d,%d," % (b['104'],b['200'],b['101'],b['103'],\
                                                 b['201'],b['106'],b['202']))
        #输出用户行业分布
        c = self.trade_dist
        fout.write("%d,%d,%d,%d,%d,%d,%d," % (c['9910'],c['9920'],c['6530'],c['6510'],\
                                              c['1710'],c['1810'],c['others']))
        #输出用户城乡分布
        d = self.urban_rural_dist
        fout.write("%d,%d,%d," % (d['01'],d['02'],d['03']))
        #输出用户分类分布
        e = self.sort_dist
        fout.write("%d,%d,%d,%d," % (e['00'],e['01'],e['02'],e['03']))
        #输出用户负荷性质分布
        f = self.load_attr_dist
        fout.write("%d,%d,%d," % (f['1'],f['2'],f['3']))
        #输出用户状态分布
        g = self.status_dist
        fout.write("%d,%d,%d," % (g['0'],g['2'],g['9']))


        #输出用户电价用户频次
        fout.write("%d," % self.cons_id_freq)
        #输出执行峰谷电价频次
        fout.write("%d," % self.ts_flag_freq)


        #输出用户是否为低保护
        fout.write("%d," % self.dibaohu_flag)
        #输出所属低保护类型
        fout.write("%d,%d," % (self.dibaohu_type['01'], self.dibaohu_type['02']))
        #输出所属低保护状态
        fout.write("%d,%d," % (self.dibaohu_status['01'], self.dibaohu_status['02']))


        #输出费控信息
        fout.write("%d,%d,%d,%d," % (self.rca_flag, self.rca_status['01'], self.rca_status['02'],\
                                     self.rca_status['03']))

        #输出延期缴费频次
        fout.write("%d," % self.pay_delay_freq)


        #输出实收电费信息
        for fee in self.monthly_rcvbl_fee:
            fout.write("%f," % fee)
        for fee in self.monthly_rcved_fee:
            fout.write("%f," % fee)
        for fee in self.monthly_rcvbl_penalty:
            fout.write("%f," % fee)
        for fee in self.monthly_rcved_penalty:
            fout.write("%f," % fee)
        for pq in self.monthly_t_pq:
             fout.write("%f," % pq)
        for fee in self.monthly_owe_amt:
             fout.write("%f," % fee)


        #输出运行电能表信息
        h = self.dianneng_type
        fout.write("%d,%d,%d,%d,%d,%d," % (h['01'],h['02'],h['03'],h['04'],h['09'],h['10']))


        #输出每月缴费次数
        for freq in self.monthly_pay_freq:
            fout.write("%d," % freq)
        #输出方式缴费次数
        i = self.typely_pay_freq
        fout.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d," % (i['020311'],i['020101'],i['020108'],i['010101'], \
                                                          i['020331'],i['030201'],i['020261'],i['020271'], \
                                                          i['010301'],i['010106'],i['010601']))

        #输出供电单位分布
        j = self.org_no_dist
        fout.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d," % (j['33402'],j['33403'],j['33404'],j['33405'], \
                                                            j['33401'],j['33406'],j['33407'],j['33408'], \
                                                            j['33409'],j['33410'],j['33411'],j['33420']))

        #输出用电类别
        k = self.elec_type_dist
        fout.write("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d," % \
                   (k['201'],k['200'],k['203'],k['202'],k['300'],k['301'],k['900'],k['404'],k['405'],k['000'], \
                    k['403'],k['402'],k['401'],k['400'],k['102'],k['100'],k['504'],k['503'],k['500'],k['101'],k['null']))



        #/*                       新增特征                      */
        #最近12个月缴费次数
        sum_freq = 0
        for freq in self.monthly_pay_freq:
            sum_freq += freq
        fout.write("%d," % sum_freq)
        #月平均缴费次数
        fout.write("%f," % round(sum_freq*1.0/12, 3))

        #最近12个月缴费方式的种类
        pay_type_cnt = 0
        for pay_type in self.typely_pay_freq:
            if self.typely_pay_freq[pay_type] > 0:
                pay_type_cnt += 1
        fout.write("%d," % pay_type_cnt)

        #最近12个月实收电费总额
        sum_fee = 0
        for fee in self.monthly_rcved_fee:
            sum_fee += fee
        fout.write("%f," % sum_fee)
        #月平均实收电费金额
        fout.write("%f," % round(sum_fee*1.0/12, 3))

        #最近12个月的违约金总额
        sum_penalty = 0
        for fee in self.monthly_rcved_penalty:
            sum_penalty += fee
        fout.write("%f," % sum_penalty)
        #月平均违约金额
        fout.write("%f," % round(sum_penalty*1.0/12, 3))

        #最近12个月用电总量
        sum_pq = 0
        for pq in self.monthly_t_pq:
            sum_pq += pq
        #总用电量等级
        if sum_pq >= 4800:
            fout.write("%d," % 3)
        elif sum_pq < 2761:
            fout.write("%d," % 1)
        else:
            fout.write("%d," % 2)


        #每月欠费金额 & 累计欠费金额
        sum_owe = 0
        owe_freq = 0
        not_owe_freq = 0
        for i in range(12):
            owe = self.monthly_rcvbl_fee[i] - self.monthly_rcved_fee[i]
            fout.write("%f," % owe)
            if owe > 0:
                sum_owe += owe
                owe_freq += 1
            elif owe == 0:
                not_owe_freq += 1
        ave_owe = 0
        if owe_freq > 0:
            ave_owe = sum_owe*1.0/owe_freq
        fout.write("%d,%d,%f,%f," % (owe_freq, not_owe_freq, sum_owe, round(ave_owe, 3)))

        #连续三月用电少于10度
        fout.write("%d," % self.check_lianxuyongdian_less_10())
        #从无电量到有电量
        fout.write("%d," % self.check_dianliang_wudaoyou())
        #从有电量到无电量
        fout.write("%d," % self.check_dianliang_youdaowu())
        #电量增加100%
        fout.write("%d," % self.check_dianliang_increase())
        #电量下降50%
        fout.write("%d," % self.check_dianliang_decrease())
        #连续三个月电量增加
        fout.write("%d," % self.check_dianliang_continue_increase())
        #连续三个月电量降低
        fout.write("%d," % self.check_dianliang_continue_decrease())


        #12个月总电量，均值，方差
        square_pq = 0
        ave_pq = sum_pq/12.0
        for pq in self.monthly_t_pq:
            square_pq += (pq - ave_pq)**2
        fout.write("%f,%f,%f," % (sum_pq, round(ave_pq, 3), round(square_pq/11.0, 3)))

        #12个月总电费，均值，方差
        sum_amt = 0
        for amt in self.monthly_owe_amt:
            sum_amt += amt
        square_amt = 0
        ave_amt = sum_amt/12.0
        for amt in self.monthly_owe_amt:
            square_amt += (amt - ave_amt)**2
        fout.write("%f,%f,%f," % (sum_amt, round(ave_amt, 3), round(square_amt/11.0, 3)))

        #每个月每度电均价
        for i in range(len(self.monthly_owe_amt)):
            month_ave_price = 0
            if self.monthly_t_pq[i] != 0:
                month_ave_price = round(self.monthly_owe_amt[i]*1.0/self.monthly_t_pq[i], 3)
            fout.write("%f," % month_ave_price)

        #每个月电量是否异常
        std_pq = math.sqrt(square_pq/11.0)
        for i in range(len(self.monthly_t_pq)):
            if abs(self.monthly_t_pq[i]-ave_pq) >= 3*std_pq:
                fout.write("%d," % 1)
            else:
                fout.write("%d," % 0)

        #每个月电费是否异常
        std_amt = math.sqrt(square_amt/11.0)
        for i in range(len(self.monthly_owe_amt)):
            if abs(self.monthly_owe_amt[i]-ave_amt) >= 3*std_amt:
                fout.write("%d," % 1)
            else:
                fout.write("%d," % 0)

        #双月电量环比变化
        for i in range(5):
            pre = self.monthly_t_pq[2*i]+self.monthly_t_pq[2*i+1]
            next = self.monthly_t_pq[2*(i+1)]+self.monthly_t_pq[2*(i+1)+1]
            if pre != 0:
                fout.write("%f," % round((next-pre)*1.0/pre, 3))
            else:
                if next > 0:
                    fout.write("%f," % 999)
                elif next < 0:
                    fout.write("%f," % -999)
                else:
                    fout.write("%f," % 0)

        #双月电费环比变化
        for i in range(5):
            pre = self.monthly_owe_amt[2*i]+self.monthly_owe_amt[2*i+1]
            next = self.monthly_owe_amt[2*(i+1)]+self.monthly_owe_amt[2*(i+1)+1]
            if pre != 0:
                fout.write("%f," % round((next-pre)*1.0/pre, 3))
            else:
                if next > 0:
                    fout.write("%f," % 999)
                elif next < 0:
                    fout.write("%f," % -999)
                else:
                    fout.write("%f," % 0)

        #每个月用电量等级
        for pq in self.monthly_t_pq:
            if pq < 230:
                fout.write("%d," % 1)
            elif pq >= 230 and pq < 400:
                fout.write("%d," % 2)
            elif pq >= 400 and pq < 920:
                fout.write("%d," % 3)
            elif pq >= 920 and pq < 1600:
                fout.write("%d," % 4)
            elif pq >= 1600:
                fout.write("%d," % 5)


        #实收金额均值方差
        sum_rcved = 0
        for fee in self.monthly_rcved_fee:
            sum_rcved += fee
        ave_rcved = sum_rcved /12.0
        square_rcved = 0
        for fee in self.monthly_rcved_fee:
            square_rcved += (fee - ave_rcved)**2
        fout.write("%f,%f," % (round(ave_rcved, 3), round(square_rcved/11.0, 3)))

        #应收金额均值方差
        sum_rcvbl = 0
        for fee in self.monthly_rcvbl_fee:
            sum_rcvbl += fee
        ave_rcvbl = sum_rcvbl /12.0
        square_rcvbl = 0
        for fee in self.monthly_rcvbl_fee:
            square_rcvbl += (fee - ave_rcvbl)**2
        fout.write("%f,%f," % (round(ave_rcvbl, 3), round(square_rcvbl/11.0, 3)))


        #双月实收环比变化
        for i in range(5):
            pre = self.monthly_rcved_fee[2*i]+self.monthly_rcved_fee[2*i+1]
            next = self.monthly_rcved_fee[2*(i+1)]+self.monthly_rcved_fee[2*(i+1)+1]
            if pre != 0:
                fout.write("%f," % round((next-pre)*1.0/pre, 3))
            else:
                if next > 0:
                    fout.write("%f," % 999)
                elif next < 0:
                    fout.write("%f," % -999)
                else:
                    fout.write("%f," % 0)

        #双月应收环比变化
        for i in range(5):
            pre = self.monthly_rcvbl_fee[2*i]+self.monthly_rcvbl_fee[2*i+1]
            next = self.monthly_rcvbl_fee[2*(i+1)]+self.monthly_rcvbl_fee[2*(i+1)+1]
            if pre != 0:
                fout.write("%f," % round((next-pre)*1.0/pre, 3))
            else:
                if next > 0:
                    fout.write("%f," % 999)
                elif next < 0:
                    fout.write("%f," % -999)
                else:
                    fout.write("%f," % 0)


        #缴费次数均值方差
        sum_pay_freq = 0
        for freq in self.monthly_pay_freq:
            sum_pay_freq += freq
        ave_pay_freq = sum_pay_freq /12.0
        square_pay_freq = 0
        for freq in self.monthly_pay_freq:
            square_pay_freq += (freq - ave_pay_freq)**2
        fout.write("%f,%f," % (round(ave_pay_freq, 3), round(square_pay_freq/11.0, 3)))


        #双月缴费次数环比变化
        for i in range(5):
            pre = self.monthly_pay_freq[2*i]+self.monthly_pay_freq[2*i+1]
            next = self.monthly_pay_freq[2*(i+1)]+self.monthly_pay_freq[2*(i+1)+1]
            if pre != 0:
                fout.write("%f," % round((next-pre)*1.0/pre, 3))
            else:
                if next > 0:
                    fout.write("%f," % 999)
                elif next < 0:
                    fout.write("%f," % -999)
                else:
                    fout.write("%f," % 0)


        #电量、实收、应收为0、负、正
        zero_freq = 0
        minus_freq = 0
        plus_freq = 0
        for pq in self.monthly_t_pq:
            if pq > 0:
                plus_freq += 1
            elif pq < 0:
                minus_freq += 1
            else:
                zero_freq += 1
        fout.write("%d,%d,%d," % (zero_freq, minus_freq, plus_freq))
        zero_freq = 0
        minus_freq = 0
        plus_freq = 0
        for fee in self.monthly_rcved_fee:
            if fee > 0:
                plus_freq += 1
            elif fee < 0:
                minus_freq += 1
            else:
                zero_freq += 1
        fout.write("%d,%d,%d," % (zero_freq, minus_freq, plus_freq))
        zero_freq = 0
        minus_freq = 0
        plus_freq = 0
        for fee in self.monthly_rcvbl_fee:
            if fee > 0:
                plus_freq += 1
            elif fee < 0:
                minus_freq += 1
            else:
                zero_freq += 1
        fout.write("%d,%d,%d," % (zero_freq, minus_freq, plus_freq))


        #应收金额上半年下半年环比
        sum_all_year = 0
        up_half = 0
        down_half = 0
        for i in range(12):
            sum_all_year += self.monthly_rcvbl_fee[i]
            if i < 6:
                up_half += self.monthly_rcvbl_fee[i]
            else:
                down_half += self.monthly_rcvbl_fee[i]
        rate = 0
        if up_half != 0:
            rate = (down_half-up_half)*1.0 / up_half
        fout.write("%f," % round(rate, 3))

        #应收上下半年占比
        rate_up = 0
        rate_down = 0
        if sum_all_year != 0:
            rate_up = up_half*1.0 / sum_all_year
            rate_down = down_half*1.0 / sum_all_year
        fout.write("%f,%f," % (round(rate_up, 3), round(rate_down, 3)))


        #实收金额上半年下半年环比
        sum_all_year = 0
        up_half = 0
        down_half = 0
        for i in range(12):
            sum_all_year += self.monthly_rcvbl_fee[i]
            if i < 6:
                up_half += self.monthly_rcved_fee[i]
            else:
                down_half += self.monthly_rcved_fee[i]
        rate = 0
        if up_half != 0:
            rate = (down_half-up_half) / up_half
        fout.write("%f," % round(rate, 3))

        #实收上下半年占比
        rate_up = 0
        rate_down = 0
        if sum_all_year != 0:
            rate_up = up_half*1.0 / sum_all_year
            rate_down = down_half*1.0 / sum_all_year
        fout.write("%f,%f," % (round(rate_up, 3), round(rate_down, 3)))

        #用电量夏季、冬季高峰占比
        summer_pq = 0
        winter_pq = 0
        pq_all_year = 0
        for i in range(12):
            pq_all_year += self.monthly_t_pq[i]
            if i == 7 or i == 8 or i == 9:
                summer_pq += self.monthly_t_pq[i]
            elif i == 10 or i == 11 or i == 12:
                winter_pq += self.monthly_t_pq[i]
        rate_summer = 0
        rate_winter = 0
        if pq_all_year != 0:
            rate_summer = round(summer_pq*1.0/pq_all_year, 3)
            rate_winter = round(winter_pq*1.0/pq_all_year, 3)
        fout.write("%f,%f," % (rate_summer, rate_winter))


        #月末缴费次数
        sum_endpay_freq = 0
        for freq in self.monthly_end_pay_freq:
            sum_endpay_freq += freq
        fout.write("%d" % sum_endpay_freq)


    @classmethod
    def output_feature_title(self, fout, content_keywords, reason_keywords):
        fout.write(utils.utf2gbk("用户编号,LABEL,"))

        # /*                    客服通话相关表特征                      */
        fout.write(utils.utf2gbk("001_致电,003_致电,005_致电,006_致电,007_致电,008_致电,009_致电,010_致电,015_致电,018_致电,"))
        fout.write(utils.utf2gbk("致电总数,平均通话时长,"))
        fout.write(utils.utf2gbk("1月催办次数,2月催办次数,3月催办次数,4月催办次数,5月催办次数,6月催办次数,7月催办次数,"))
        fout.write(utils.utf2gbk("8月催办次数,9月催办次数,10月催办次数,11月催办次数,12月催办次数,"))

        #文本特征
        fout.write(utils.utf2gbk("催办电费"))
        sort_keywords = sorted(content_keywords.iteritems(), key=lambda x:x[1])
        for keyword,idx in sort_keywords:
            fout.write(",C_%s" % utils.utf2gbk(keyword))

        '''
        sort_reasons = sorted(reason_keywords.iteritems(), key=lambda x:x[1])
        for reason,idx in sort_reasons:
            fout.write(",R_%s" % utils.utf2gbk(reason))
        '''


        # /*                    用电信息相关表特征                      */
        fout.write(utils.utf2gbk(",合同容量,"))
        fout.write(utils.utf2gbk("104水泥,200其他,101钢铁,103铁合金,201造纸,106烧碱,202铸造,"))
        fout.write(utils.utf2gbk("9910城镇,9920乡村,6530纺织,6510零售,1710印染,1810服装,其他,"))
        fout.write(utils.utf2gbk("01城乡,02城乡,03城乡,"))
        fout.write(utils.utf2gbk("00分类,01分类,02分类,03分类,"))
        fout.write(utils.utf2gbk("1负荷,2负荷,3负荷,"))
        fout.write(utils.utf2gbk("0状态,2状态,9状态,"))
        fout.write(utils.utf2gbk("电价频次,执行峰谷频次,"))
        fout.write(utils.utf2gbk("是否低保户,低保户类型01,低保户类型02,低保户状态01,低保户状态02,"))
        fout.write(utils.utf2gbk("是否费控,费控状态1,费控状态2,费控状态3,"))
        fout.write(utils.utf2gbk("延期缴费频次,"))
        fout.write(utils.utf2gbk("1月应收F,2月应收F,3月应收F,4月应收F,5月应收F,6月应收F,7月应收F,"))
        fout.write(utils.utf2gbk("8月应收F,9月应收F,10月应收F,11月应收F,12月应收F,"))
        fout.write(utils.utf2gbk("1月实收F,2月实收F,3月实收F,4月实收F,5月实收F,6月实收F,7月实收F,"))
        fout.write(utils.utf2gbk("8月实收F,9月实收F,10月实收F,11月实收F,12月实收F,"))
        fout.write(utils.utf2gbk("1月应收P,2月应收P,3月应收P,4月应收P,5月应收P,6月应收P,7月应收P,"))
        fout.write(utils.utf2gbk("8月应收P,9月应收P,10月应收P,11月应收P,12月应收P,"))
        fout.write(utils.utf2gbk("1月实收P,2月实收P,3月实收P,4月实收P,5月实收P,6月实收P,7月实收P,"))
        fout.write(utils.utf2gbk("8月实收P,9月实收P,10月实收P,11月实收P,12月实收P,"))
        fout.write(utils.utf2gbk("1月电量,2月电量,3月电量,4月电量,5月电量,6月电量,7月电量,"))
        fout.write(utils.utf2gbk("8月电量,9月电量,10月电量,11月电量,12月电量,"))
        fout.write(utils.utf2gbk("1月总电费,2月总电费,3月总电费,4月总电费,5月总电费,6月总电费,7月总电费,"))
        fout.write(utils.utf2gbk("8月总电费,9月总电费,10月总电费,11月总电费,12月总电费,"))
        fout.write(utils.utf2gbk("01电能表,02电能表,03电能表,04电能表,09电能表,10电能表,"))

        fout.write(utils.utf2gbk("1月缴费Q,2月缴费Q,3月缴费Q,4月缴费Q,5月缴费Q,6月缴费Q,7月缴费Q,"))
        fout.write(utils.utf2gbk("8月缴费Q,9月缴费Q,10月缴费Q,11月缴费Q,12月缴费Q,"))
        fout.write(utils.utf2gbk("20311缴费,20101缴费,20108缴费,10101缴费,20331缴费,"))
        fout.write(utils.utf2gbk("30201缴费,20261缴费,20271缴费,10301缴费,10106缴费,10601缴费,"))
        fout.write(utils.utf2gbk("供电单位33402,供电单位33403,供电单位33404,供电单位33405,"))
        fout.write(utils.utf2gbk("供电单位33401,供电单位33406,供电单位33407,供电单位33408,"))
        fout.write(utils.utf2gbk("供电单位33409,供电单位33410,供电单位33411,供电单位33420,"))
        fout.write(utils.utf2gbk("用电201,用电200,用电203,用电202,用电300,用电301,用电900,"))
        fout.write(utils.utf2gbk("用电404,用电405,用电000,用电403,用电402,用电401,用电400,"))
        fout.write(utils.utf2gbk("用电102,用电100,用电504,用电503,用电500,用电101,用电null,"))

        fout.write(utils.utf2gbk("最近12个月缴费次数,"))
        fout.write(utils.utf2gbk("月平均缴费次数,"))
        fout.write(utils.utf2gbk("缴费方式种类,"))
        fout.write(utils.utf2gbk("实收电费总额,月平均实收电费,"))
        fout.write(utils.utf2gbk("实收违约金总额,月平均实收违约金,"))
        fout.write(utils.utf2gbk("用电等级,"))
        fout.write(utils.utf2gbk("1月欠费,2月欠费,3月欠费,4月欠费,5月欠费,6月欠费,"))
        fout.write(utils.utf2gbk("7月欠费,8月欠费,9月欠费,10月欠费,11月欠费,12月欠费,"))
        fout.write(utils.utf2gbk("欠费大于0,欠费等于0,累计欠费金额,平均欠费金额,"))
        fout.write(utils.utf2gbk("连续用电少于10,"))
        fout.write(utils.utf2gbk("电量从无到有,电量从有到无,"))
        fout.write(utils.utf2gbk("电量增加,电量减少,"))
        fout.write(utils.utf2gbk("电量连续增加,电量连续减少,"))
        fout.write(utils.utf2gbk("总电量,电量均值,电量方差,"))
        fout.write(utils.utf2gbk("总电费,电费均值,电费方差,"))
        fout.write(utils.utf2gbk("1月均价,2月均价,3月均价,4月均价,5月均价,6月均价,"))
        fout.write(utils.utf2gbk("7月均价,8月均价,9月均价,10月均价,11月均价,12月均价,"))
        fout.write(utils.utf2gbk("1月电量异常,2月电量异常,3月电量异常,4月电量异常,5月电量异常,6月电量异常,"))
        fout.write(utils.utf2gbk("7月电量异常,8月电量异常,9月电量异常,10月电量异常,11月电量异常,12月电量异常,"))
        fout.write(utils.utf2gbk("1月电费异常,2月电费异常,3月电费异常,4月电费异常,5月电费异常,6月电费异常,"))
        fout.write(utils.utf2gbk("7月电费异常,8月电费异常,9月电费异常,10月电费异常,11月电费异常,12月电费异常,"))
        fout.write(utils.utf2gbk("3-4电量环比,5-6电量环比,7-8电量环比,9-10电量环比,11-12电量环比,"))
        fout.write(utils.utf2gbk("3-4电费环比,5-6电费环比,7-8电费环比,9-10电费环比,11-12电费环比,"))

        fout.write(utils.utf2gbk("1月电量档次,2月电量档次,3月电量档次,4月电量档次,5月电量档次,6月电量档次,"))
        fout.write(utils.utf2gbk("7月电量档次,8月电量档次,9月电量档次,10月电量档次,11月电量档次,12月电量档次,"))
        fout.write(utils.utf2gbk("实收金额均值,实收金额方差,"))
        fout.write(utils.utf2gbk("应收金额均值,应收金额方差,"))
        fout.write(utils.utf2gbk("3-4实收环比,5-6实收环比,7-8实收环比,9-10实收环比,11-12实收环比,"))
        fout.write(utils.utf2gbk("3-4应收环比,5-6应收环比,7-8应收环比,9-10应收环比,11-12应收环比,"))
        fout.write(utils.utf2gbk("缴费次数均值,缴费次数方差,"))
        fout.write(utils.utf2gbk("3-4次数环比,5-6次数环比,7-8次数环比,9-10次数环比,11-12次数环比,"))
        fout.write(utils.utf2gbk("电量为0月数,电量为负月数,电量为正月数,"))
        fout.write(utils.utf2gbk("实收为0月数,实收为负月数,实收为正月数,"))
        fout.write(utils.utf2gbk("应收为0月数,应收为负月数,应收为正月数,"))
        fout.write(utils.utf2gbk("应收下半年环比,实收下半年环比,"))
        fout.write(utils.utf2gbk("应收上半年占比,应收下半年占比,"))
        fout.write(utils.utf2gbk("实收上半年占比,实收下半年占比,"))
        fout.write(utils.utf2gbk("夏季用电占比,冬季用电占比,"))


        fout.write(utils.utf2gbk("月末缴费次数"))

        fout.write('\n')