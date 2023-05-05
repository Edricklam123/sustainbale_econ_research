# Import libraries
rm(list=ls())
library(plm)
library(stargazer)
library(tidyverse)
options(scipen = 10)

setwd("C:/Users/Edrick/PycharmProjects/sustainbale_econ_research/da_working_files")
df = read.csv('df_panel_master.csv', na.strings = '#N/A N/A NA')
df_all_comps = read.csv('df_all_comps_with_power.csv', na.strings = '#N/A N/A NA')
df_backup = df
df = df_backup
head(df)
df = df[,-1]

# XXX
df$ln_cp_avg_price_sq = df$ln_cp_avg_prce^2
df$ln_total_carbon_emission = log(df$total_carbon_emission)
pdf = pdata.frame(df, index = c('entity_id', 'year'), row.names = F, drop.NA.series = T)
names(pdf)

# Running models
pool1 = plm(ln_abs_ghg_scope_1~ln_cp_avg_prce, data=pdf, model='pooling')
summary(pool1)

pool2 = plm(absolute_ghg_scope_1~ln_cp_avg_prce, data=pdf, model='pooling')
summary(pool2)

pool3 = plm(ln_abs_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq, data=pdf, model='pooling')
summary(pool3)

pool4 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq, data=pdf, model='pooling')
summary(pool4)



fe1 = plm(absolute_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='time')
summary(fe1)

fe2 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='time')
summary(fe2)

fe3 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='individual')
summary(fe3)

fe4 = plm(ln_intensity_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within', effect='time')
summary(fe4)

fe3 = plm(ln_total_carbon_emission~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='within')
summary(fe3)



re1 = plm(absolute_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
          +ln_fx_asset, data=pdf, model='random')
plmtest(re1, type='bp')

phtest(fe1, re1)


# Models
names(df)
fe1 = lm(ln_intensity_ghg_scope_1~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
         +ln_fx_asset + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(log(total_carbon_emission)~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
           +log() + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
        +I(log(tot_asset)) +ln_fx_asset + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_cp_avg_prce_sq+ln_lt_debt
         +I(log(tot_asset)) +ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe_star = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_lt_debt
         +I(log(tot_asset)) +ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(fe1)

fe1 = lm(I(log(total_carbon_emission))~I(log(cp_avg_price))+I(log(lt_debt))
         +I(log(tot_asset)) +I(log(fx_asset)) + I(log(mkt_cap)) + factor(entity_id) + factor(year), data=df)
summary(fe1)


# ---------------------------------------
# Model for Carbon Pricing
# ---------------------------------------
cp_scp1_0 = lm(I(log(absolute_ghg_scope_1))~ln_cp_avg_prce
                  + factor(entity_id) + factor(year), data=df)
summary(cp_scp1_0)

cp_scp1_1 = lm(I(log(absolute_ghg_scope_1))~ln_cp_avg_prce+ln_lt_debt
                   + factor(entity_id) + factor(year), data=df)
summary(cp_scp1_1)

cp_scp1_2 = lm(I(log(absolute_ghg_scope_1))~ln_cp_avg_prce+ln_lt_debt
                  +I(log(tot_asset)) + factor(entity_id) + factor(year), data=df)
summary(cp_scp1_2)

cp_scp1_3 = lm(I(log(absolute_ghg_scope_1))~ln_cp_avg_prce+ln_lt_debt
                  +I(log(tot_asset)) + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(cp_scp1_3)

cp_scp1_4 = lm(I(log(absolute_ghg_scope_1))~ln_cp_avg_prce+ln_lt_debt
                  +I(log(tot_asset)) + ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(cp_scp1_4)

stargazer(cp_scp1_0, cp_scp1_1, cp_scp1_2, cp_scp1_3, cp_scp1_4, type='text')
stargazer(cp_scp1_0, cp_scp1_1, cp_scp1_2, cp_scp1_3, cp_scp1_4, type='html', out='CP_tb1.html')

# Comparison
cp_scp1_4 = lm(I(log(absolute_ghg_scope_1))~ln_cp_avg_prce+ln_lt_debt
               +I(log(tot_asset)) + ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(cp_scp1_4)

cp_scp2_4 = lm(I(log(absolute_ghg_scope_2))~ln_cp_avg_prce+ln_lt_debt
            +I(log(tot_asset)) +ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(cp_scp2_4)

cp_fe_tot_4 = lm(I(log(total_carbon_emission))~ln_cp_avg_prce+ln_lt_debt
            +I(log(tot_asset)) +ln_fx_asset + ln_mkt_cap + factor(entity_id) + factor(year), data=df)
summary(cp_fe_tot_4)

stargazer(cp_scp1_4, cp_scp2_4, cp_fe_tot_4, type='text')
stargazer(cp_scp1_4, cp_scp2_4, cp_fe_tot_4, type='html', out='CP_tb2.html')

# ---------------------------------------
# Model for green tech ratio
# ---------------------------------------
fe1 = lm(green_tech_rr~I(log(cp_avg_price))+I(log(lt_debt))
         +I(log(tot_asset)) +I(log(fx_asset)) + I(log(mkt_cap)) + factor(entity_id) + factor(year), data=df)
summary(fe1)
stargazer(fe1, type='text')
stargazer(fe1, type='html', out='CP_tb3.html')

names(df_all_comps)
fe2 = lm(green_tech_rr~I(log(cp_avg_price))  + factor(entity_id) + factor(year), data=df_all_comps)
summary(fe2)
coef(fe2)
stargazer(fe2, type='html', out='CP_tb4.html')

fe3 = lm(green_tech_rr~I(log(cp_avg_price)) + factor(entity_id) + factor(year), data=df)
summary(fe3)
stargazer(fe3, type='html', out='CP_tb5.html')

str(df)
