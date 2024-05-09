



def perbandingan(start_date, end_date):

    if start_date is not None and end_date is not None:
        date_filter = f"""
            AND bt.created_at BETWEEN '{start_date}' AND '{end_date}'::date + INTERVAL '1 DAY'
            """
    else:
        date_filter = ""       

    sql = f"""
            select 
                bb.jenis_barang 
                , a.transaksi
            from backend_barang bb 
            left join (
                select 
                    bb2.jenis_barang 
                    , sum(bt.jumlah) as transaksi 
                from backend_transaksi bt 
                join backend_barang bb2 on bb2.id = bt.barang_id
                where bt.deleted_at is null and bt.jenis_transaksi = 'jual'
                {date_filter}
                group by bb2.jenis_barang
            ) a on a.jenis_barang = bb.jenis_barang
            group by bb.jenis_barang, a.transaksi

    """

    return sql