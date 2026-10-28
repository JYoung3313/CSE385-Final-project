-- select vendor_state, vendor_city, count(*) as invoice_qty,
-- 	round(Avg(invoice_total), 2) as invoice_avg
-- from invoices join vendors
-- 	on invoices.vendor_id = vendors.vendor_id
-- group by vendor_state, vendor_city
-- order by vendor_state, vendor_city asc

select invoice_date,
	count(*) as invoice_qty,
    sum(invoice_total) as invoice_sum
from invoices
where invoice_date between '2022-05-01' and '2022-05-31'
group by invoice_date
having count(*) > 1
	and sum(invoice_total) > 100
order by invoice_date desc